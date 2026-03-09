"""MCP Server 1: study-engine — session management and FSRS scheduling."""

from __future__ import annotations

import json
from datetime import datetime
from typing import Any

from mcp.server.fastmcp import FastMCP
from sqlalchemy.ext.asyncio import AsyncSession

from cert_pepper.db.connection import get_session, init_db
from cert_pepper.engine import fsrs, selector
from cert_pepper.models.content import Question

mcp = FastMCP("cert-pepper-study-engine")

# In-memory session state (simple single-user)
_sessions: dict[str, dict[str, Any]] = {}


async def _get_user_id(session: AsyncSession) -> int:
    from sqlalchemy import text

    result = await session.execute(text("SELECT id FROM users WHERE username='default' LIMIT 1"))
    row = result.fetchone()
    return int(row[0]) if row else 1


async def _get_question(session: AsyncSession, question_id: int) -> Question | None:
    from sqlalchemy import text

    result = await session.execute(
        text("""
            SELECT q.id, q.domain_id, d.number, q.number, q.stem,
                   q.option_a, q.option_b, q.option_c, q.option_d,
                   q.correct_answer, q.explanation, q.difficulty, q.source_file
            FROM questions q JOIN domains d ON d.id = q.domain_id
            WHERE q.id = :qid
        """),
        {"qid": question_id},
    )
    row = result.fetchone()
    if not row:
        return None
    return Question(
        id=row[0],
        domain_id=row[1],
        domain_number=row[2],
        number=row[3],
        stem=row[4],
        option_a=row[5],
        option_b=row[6],
        option_c=row[7],
        option_d=row[8],
        correct_answer=row[9],
        explanation=row[10],
        difficulty=row[11],
        source_file=row[12],
    )


@mcp.tool()
async def start_session(
    session_type: str = "study",
    domain_filter: int | None = None,
    exam_code: str | None = None,
    new_only: bool = False,
) -> str:
    """Start a new study session. Returns session_id."""
    from sqlalchemy import text

    from cert_pepper.db.exams import resolve_cert_id

    async with get_session() as db:
        user_id = await _get_user_id(db)
        try:
            cert_id = await resolve_cert_id(db, exam_code)
        except ValueError as e:
            return json.dumps({"error": str(e)})

        # Get the exam code to return
        result = await db.execute(
            text("SELECT code FROM certifications WHERE id = :cid"),
            {"cid": cert_id},
        )
        cert_code = result.scalar() or exam_code

        await db.execute(
            text(
                "INSERT INTO study_sessions"
                " (user_id, session_type, domain_filter, certification_id)"
                " VALUES (:uid, :type, :domain, :cert_id)"
            ),
            {"uid": user_id, "type": session_type, "domain": domain_filter, "cert_id": cert_id},
        )
        result = await db.execute(text("SELECT last_insert_rowid()"))
        id_row = result.fetchone()
        session_db_id = int(id_row[0]) if id_row else 0

    session_id = f"sess_{session_db_id}"
    _sessions[session_id] = {
        "db_id": session_db_id,
        "type": session_type,
        "domain_filter": domain_filter,
        "cert_id": cert_id,
        "new_only": new_only,
        "questions_seen": 0,
        "questions_correct": 0,
        "started_at": datetime.utcnow().isoformat(),
    }

    return json.dumps({
        "session_id": session_id,
        "session_type": session_type,
        "domain_filter": domain_filter,
        "exam_code": cert_code,
        "message": "Study session started. Use get_next_question to begin.",
    })


@mcp.tool()
async def get_next_question(session_id: str) -> str:
    """Get the next question for a study session. Uses adaptive selection."""
    sess = _sessions.get(session_id, {})
    domain_filter = sess.get("domain_filter")
    cert_id = sess.get("cert_id")
    new_only = sess.get("new_only", False)

    async with get_session() as db:
        user_id = await _get_user_id(db)
        question_id = await selector.select_question(
            db, user_id, domain_filter=domain_filter, cert_id=cert_id, new_only=new_only
        )

        if question_id is None:
            return json.dumps({
                "error": "No questions available. Try running cert-pepper ingest first."
            })

        q = await _get_question(db, question_id)
        if q is None:
            return json.dumps({"error": "Question not found."})

    return json.dumps({
        "question_id": q.id,
        "domain": q.domain_number,
        "question_number": q.number,
        "stem": q.stem,
        "options": q.options_dict(),
        "hint": "Use submit_answer with your selection (A/B/C/D) and fsrs_rating (1-4).",
    })


@mcp.tool()
async def submit_answer(
    session_id: str,
    question_id: int,
    answer: str,
    time_seconds: float = 0,
    fsrs_rating: int = 3,
) -> str:
    """Submit an answer and get feedback + FSRS scheduling update.

    fsrs_rating: 1=Again, 2=Hard, 3=Good, 4=Easy
    """
    from sqlalchemy import text

    answer = answer.upper()

    async with get_session() as db:
        user_id = await _get_user_id(db)
        q = await _get_question(db, question_id)
        if q is None:
            return json.dumps({"error": "Question not found."})

        is_correct = answer == q.correct_answer

        # Update FSRS
        result = await db.execute(
            text("""
                SELECT stability, difficulty, retrievability, due_date,
                       last_review, state, step, reps, lapses
                FROM fsrs_cards WHERE user_id=:uid AND content_type='question' AND content_id=:qid
            """),
            {"uid": user_id, "qid": question_id},
        )
        row = result.fetchone()
        if row:
            card = fsrs.FSRSCard(
                stability=row[0],
                difficulty=row[1],
                retrievability=row[2],
                due_date=datetime.fromisoformat(str(row[3])),
                last_review=datetime.fromisoformat(str(row[4])) if row[4] else None,
                state=row[5],
                step=row[6],
                reps=row[7],
                lapses=row[8],
            )
        else:
            card = fsrs.FSRSCard()

        updated = fsrs.schedule(card, fsrs_rating)
        await db.execute(
            text("""
                INSERT INTO fsrs_cards
                    (user_id, content_type, content_id, stability, difficulty, retrievability,
                     due_date, last_review, state, step, reps, lapses)
                VALUES (:uid, 'question', :qid, :s, :d, :r,
                        :due, :last, :state, :step, :reps, :lapses)
                ON CONFLICT(user_id, content_type, content_id) DO UPDATE SET
                    stability=excluded.stability, difficulty=excluded.difficulty,
                    retrievability=excluded.retrievability, due_date=excluded.due_date,
                    last_review=excluded.last_review, state=excluded.state,
                    step=excluded.step, reps=excluded.reps, lapses=excluded.lapses
            """),
            {
                "uid": user_id,
                "qid": question_id,
                "s": updated.stability,
                "d": updated.difficulty,
                "r": updated.retrievability,
                "due": updated.due_date.isoformat(),
                "last": updated.last_review.isoformat() if updated.last_review else None,
                "state": updated.state,
                "step": updated.step,
                "reps": updated.reps,
                "lapses": updated.lapses,
            },
        )

        # Record attempt
        sess = _sessions.get(session_id, {})
        sess_db_id = sess.get("db_id", 0)
        await db.execute(
            text("""
                INSERT INTO question_attempts
                    (session_id, user_id, question_id, selected_answer,
                     is_correct, time_taken_seconds)
                VALUES (:sid, :uid, :qid, :ans, :correct, :time)
            """),
            {
                "sid": sess_db_id,
                "uid": user_id,
                "qid": question_id,
                "ans": answer,
                "correct": 1 if is_correct else 0,
                "time": time_seconds,
            },
        )

        if session_id in _sessions:
            _sessions[session_id]["questions_seen"] = (
                _sessions[session_id].get("questions_seen", 0) + 1
            )
            if is_correct:
                _sessions[session_id]["questions_correct"] = (
                    _sessions[session_id].get("questions_correct", 0) + 1
                )

    result_data: dict[str, Any] = {
        "correct": is_correct,
        "correct_answer": q.correct_answer,
        "correct_option": q.get_option(q.correct_answer),
        "explanation": q.explanation if q.explanation else "No pre-stored explanation.",
        "fsrs_state": updated.state,
        "next_review_days": fsrs.days_until_due(updated),
    }

    if not is_correct:
        result_data["your_answer"] = answer
        result_data["your_option"] = q.get_option(answer)

    return json.dumps(result_data)


@mcp.tool()
async def get_due_cards(limit: int = 20, exam_code: str | None = None) -> str:
    """Get FSRS cards due for review today."""
    from sqlalchemy import text

    async with get_session() as db:
        user_id = await _get_user_id(db)

        if exam_code:
            result = await db.execute(
                text("""
                    SELECT fc.content_id, fc.state, fc.due_date, fc.stability,
                           fc.difficulty, fc.reps, q.stem
                    FROM fsrs_cards fc
                    JOIN questions q ON q.id = fc.content_id AND fc.content_type='question'
                    JOIN domains d ON d.id = q.domain_id
                    JOIN certifications c ON c.id = d.certification_id AND c.code = :exam_code
                    WHERE fc.user_id=:uid AND fc.due_date <= CURRENT_TIMESTAMP
                    ORDER BY fc.due_date ASC
                    LIMIT :limit
                """),
                {"uid": user_id, "limit": limit, "exam_code": exam_code},
            )
        else:
            result = await db.execute(
                text("""
                    SELECT fc.content_id, fc.state, fc.due_date, fc.stability,
                           fc.difficulty, fc.reps, q.stem
                    FROM fsrs_cards fc
                    JOIN questions q ON q.id = fc.content_id AND fc.content_type='question'
                    WHERE fc.user_id=:uid AND fc.due_date <= CURRENT_TIMESTAMP
                    ORDER BY fc.due_date ASC
                    LIMIT :limit
                """),
                {"uid": user_id, "limit": limit},
            )
        rows = result.fetchall()

    cards = [
        {
            "question_id": row[0],
            "state": row[1],
            "due_date": str(row[2]),
            "stability_days": round(row[3], 2),
            "difficulty": round(row[4], 2),
            "reps": row[5],
            "preview": row[6][:100] + "..." if len(row[6]) > 100 else row[6],
        }
        for row in rows
    ]

    return json.dumps({"due_count": len(cards), "cards": cards})


@mcp.tool()
async def end_session(session_id: str) -> str:
    """End a study session and get a summary."""
    from sqlalchemy import text

    sess = _sessions.pop(session_id, {})
    sess_db_id = sess.get("db_id", 0)
    seen = sess.get("questions_seen", 0)
    correct = sess.get("questions_correct", 0)

    async with get_session() as db:
        await db.execute(
            text("""
                UPDATE study_sessions SET
                    ended_at=CURRENT_TIMESTAMP,
                    questions_seen=:seen,
                    questions_correct=:correct
                WHERE id=:sid
            """),
            {"seen": seen, "correct": correct, "sid": sess_db_id},
        )

    accuracy = correct / seen if seen > 0 else 0
    return json.dumps({
        "session_id": session_id,
        "questions_seen": seen,
        "questions_correct": correct,
        "accuracy": f"{accuracy:.0%}",
        "message": "Session ended. Run cert-pepper progress to see your full dashboard.",
    })


@mcp.tool()
async def get_session_wrong_answers(session_id: int | None = None) -> str:
    """Get wrong answers from a study or exam session.

    If session_id is None, uses the most recent completed session.
    Returns question details and what you answered vs. the correct answer,
    so you can call get_explanation() on each for AI explanations.
    """
    from sqlalchemy import text

    async with get_session() as db:
        user_id = await _get_user_id(db)

        if session_id is None:
            result = await db.execute(
                text("""
                    SELECT id, session_type, questions_seen, questions_correct
                    FROM study_sessions
                    WHERE user_id = :uid AND ended_at IS NOT NULL
                    ORDER BY ended_at DESC LIMIT 1
                """),
                {"uid": user_id},
            )
            row = result.fetchone()
            if not row:
                return json.dumps({
                    "error": "No completed sessions found. Run cert-pepper study first."
                })
            session_id, session_type, total_answered, total_correct = (
                int(row[0]), row[1], row[2], row[3]
            )
        else:
            result = await db.execute(
                text("""
                    SELECT session_type, questions_seen, questions_correct
                    FROM study_sessions
                    WHERE id = :sid AND user_id = :uid
                """),
                {"sid": session_id, "uid": user_id},
            )
            row = result.fetchone()
            if not row:
                return json.dumps({"error": f"Session {session_id} not found."})
            session_type, total_answered, total_correct = row[0], row[1], row[2]

        result = await db.execute(
            text("""
                SELECT qa.question_id, qa.selected_answer, qa.time_taken_seconds,
                       q.stem, q.correct_answer,
                       q.option_a, q.option_b, q.option_c, q.option_d,
                       d.number AS domain_number
                FROM question_attempts qa
                JOIN questions q ON q.id = qa.question_id
                JOIN domains d ON d.id = q.domain_id
                WHERE qa.session_id = :session_id AND qa.is_correct = 0
                ORDER BY qa.id
            """),
            {"session_id": session_id},
        )
        wrong_rows = result.fetchall()

    wrong_answers = [
        {
            "question_id": row[0],
            "domain": row[9],
            "stem": row[3],
            "options": {"A": row[5], "B": row[6], "C": row[7], "D": row[8]},
            "your_answer": row[1],
            "correct_answer": row[4],
            "time_seconds": row[2],
            "hint": (
                f"Call get_explanation(question_id={row[0]}, selected_answer='{row[1]}')"
                " for AI explanation"
            ),
        }
        for row in wrong_rows
    ]

    accuracy = f"{total_correct / total_answered:.0%}" if total_answered > 0 else "0%"
    return json.dumps({
        "session_id": session_id,
        "session_type": session_type,
        "wrong_count": len(wrong_answers),
        "total_answered": total_answered,
        "accuracy": accuracy,
        "wrong_answers": wrong_answers,
    })


@mcp.resource("progress://daily")
async def daily_progress() -> str:
    """Today's study statistics."""
    from sqlalchemy import text

    async with get_session() as db:
        user_id = await _get_user_id(db)
        result = await db.execute(
            text("""
                SELECT COUNT(*), SUM(is_correct)
                FROM question_attempts
                WHERE user_id=:uid AND date(created_at)=date('now')
            """),
            {"uid": user_id},
        )
        row = result.fetchone()
        assert row is not None
        total = row[0] or 0
        correct = row[1] or 0
        acc = correct / total if total > 0 else 0

    data = {
        "date": datetime.utcnow().strftime("%Y-%m-%d"),
        "questions_today": total,
        "correct_today": correct,
        "accuracy": f"{acc:.0%}",
    }
    return json.dumps(data)


@mcp.resource("progress://weak-areas")
async def weak_areas() -> str:
    """Domains below 70% accuracy."""
    from cert_pepper.db.exams import resolve_cert_id
    from cert_pepper.engine.scorer import get_weak_areas

    async with get_session() as db:
        user_id = await _get_user_id(db)
        try:
            cert_id = await resolve_cert_id(db)
        except ValueError:
            cert_id = None
        weak = await get_weak_areas(db, user_id, cert_id=cert_id)

    data = [
        {
            "domain": w.domain_number,
            "name": w.domain_name,
            "accuracy": f"{w.accuracy_pct:.0%}",
            "weight": f"{w.weight_pct:.0f}%",
            "attempts": w.attempts,
        }
        for w in weak
    ]
    return json.dumps(data)


def serve() -> None:
    """Entry point for the study-engine MCP server (stdio transport)."""
    import asyncio

    asyncio.run(init_db())
    mcp.run(transport="stdio")


if __name__ == "__main__":
    serve()
