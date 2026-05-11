"""Tests for study-engine MCP tools (TDD)."""

from __future__ import annotations

import json

from sqlalchemy import text

from tests.conftest import get_user_id, seed_question


class TestStudySessionReconnect:
    async def test_submit_answer_recovers_persisted_session_after_memory_loss(self, db):
        from cert_pepper.db.connection import get_session
        from cert_pepper.mcp.study_engine import _sessions, start_session, submit_answer
        from tests.conftest import seed_question

        async with get_session() as session:
            question_id = await seed_question(
                session, domain_number=4, number=1, correct_answer="A"
            )

        session_data = json.loads(await start_session(session_type="study"))
        session_id = session_data["session_id"]
        db_session_id = int(session_id.removeprefix("sess_"))

        _sessions.clear()

        result = json.loads(await submit_answer(session_id, question_id=question_id, answer="A"))

        assert "error" not in result

        from cert_pepper.db.connection import get_session

        async with get_session() as session:
            attempt = await session.execute(
                text(
                    "SELECT session_id, question_id, selected_answer"
                    " FROM question_attempts ORDER BY id DESC LIMIT 1"
                )
            )
            row = attempt.fetchone()

        assert row is not None
        assert row[0] == db_session_id
        assert row[1] == question_id
        assert row[2] == "A"

    async def test_get_next_question_preserves_new_only_after_memory_loss(self, db):
        from cert_pepper.db.connection import get_session
        from cert_pepper.mcp.study_engine import _sessions, get_next_question, start_session
        from tests.conftest import get_user_id, seed_question

        async with get_session() as session:
            user_id = await get_user_id(session)
            unseen_question_id = await seed_question(
                session, domain_number=4, number=1, stem="Unseen question?", correct_answer="B"
            )
            seen_question_id = await seed_question(
                session, domain_number=4, number=2, stem="Seen question?", correct_answer="C"
            )
            await session.execute(
                text("""
                    INSERT INTO fsrs_cards
                        (user_id, content_type, content_id, stability, difficulty, retrievability,
                         due_date, last_review, state, step, reps, lapses)
                    VALUES (:uid, 'question', :qid, 1.0, 5.0, 0.9,
                            CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'review', 0, 1, 0)
                """),
                {"uid": user_id, "qid": seen_question_id},
            )

        session_data = json.loads(await start_session(session_type="study", new_only=True))
        session_id = session_data["session_id"]

        _sessions.clear()

        result = json.loads(await get_next_question(session_id))

        assert "error" not in result
        assert result["question_id"] == unseen_question_id


class TestStartSessionExamSelection:
    async def test_start_session_returns_selection_required_when_multiple_exams_exist(self, db):
        from cert_pepper.db.connection import get_session
        from cert_pepper.mcp.study_engine import start_session
        from tests.conftest import seed_certification

        async with get_session() as session:
            await seed_certification(session, "AWS-SAA", "AWS Solutions Architect")
            await session.commit()

        result = json.loads(await start_session(session_type="study"))

        assert result["status"] == "selection_required"
        assert "message" in result
        assert result["options"] == [
            {"code": "AWS-SAA", "name": "AWS Solutions Architect"},
            {"code": "SY0-701", "name": "CompTIA Security+"},
        ]

    async def test_start_session_still_resolves_explicit_exam_code(self, db):
        from cert_pepper.mcp.study_engine import start_session

        result = json.loads(await start_session(session_type="study", exam_code="SY0-701"))

        assert "error" not in result
        assert result["exam_code"] == "SY0-701"
        assert result["session_id"].startswith("sess_")


class TestGetSessionWrongAnswers:
    async def test_returns_error_when_no_sessions(self, db):
        from cert_pepper.mcp.study_engine import get_session_wrong_answers

        result = json.loads(await get_session_wrong_answers())
        assert "error" in result

    async def test_returns_wrong_answers_from_last_session(self, db):
        from cert_pepper.db.connection import get_session
        from cert_pepper.mcp.study_engine import get_session_wrong_answers

        async with get_session() as session:
            user_id = await get_user_id(session)
            q1_id = await seed_question(session, number=1, correct_answer="A")
            q2_id = await seed_question(session, number=2, correct_answer="B")

            await session.execute(
                text(
                    "INSERT INTO study_sessions (user_id, session_type, ended_at,"
                    " questions_seen, questions_correct)"
                    " VALUES (:uid, 'study', CURRENT_TIMESTAMP, 2, 1)"
                ),
                {"uid": user_id},
            )
            result = await session.execute(text("SELECT last_insert_rowid()"))
            sess_id = result.scalar()

            # correct
            await session.execute(
                text(
                    "INSERT INTO question_attempts"
                    " (session_id, user_id, question_id, selected_answer, is_correct)"
                    " VALUES (:sid, :uid, :qid, 'A', 1)"
                ),
                {"sid": sess_id, "uid": user_id, "qid": q1_id},
            )
            # wrong
            await session.execute(
                text(
                    "INSERT INTO question_attempts"
                    " (session_id, user_id, question_id, selected_answer, is_correct)"
                    " VALUES (:sid, :uid, :qid, 'C', 0)"
                ),
                {"sid": sess_id, "uid": user_id, "qid": q2_id},
            )

        result = json.loads(await get_session_wrong_answers())
        assert result["session_id"] == sess_id
        assert result["session_type"] == "study"
        assert result["wrong_count"] == 1
        assert result["total_answered"] == 2
        wrong = result["wrong_answers"]
        assert len(wrong) == 1
        assert wrong[0]["question_id"] == q2_id
        assert wrong[0]["your_answer"] == "C"
        assert wrong[0]["correct_answer"] == "B"

    async def test_explicit_session_id(self, db):
        from cert_pepper.db.connection import get_session
        from cert_pepper.mcp.study_engine import get_session_wrong_answers

        async with get_session() as session:
            user_id = await get_user_id(session)
            q1_id = await seed_question(session, number=1, correct_answer="A")

            await session.execute(
                text(
                    "INSERT INTO study_sessions (user_id, session_type, ended_at,"
                    " questions_seen, questions_correct)"
                    " VALUES (:uid, 'exam', CURRENT_TIMESTAMP, 1, 0)"
                ),
                {"uid": user_id},
            )
            result = await session.execute(text("SELECT last_insert_rowid()"))
            sess_id = result.scalar()

            await session.execute(
                text(
                    "INSERT INTO question_attempts"
                    " (session_id, user_id, question_id, selected_answer, is_correct)"
                    " VALUES (:sid, :uid, :qid, 'D', 0)"
                ),
                {"sid": sess_id, "uid": user_id, "qid": q1_id},
            )

        result = json.loads(await get_session_wrong_answers(session_id=sess_id))
        assert result["session_id"] == sess_id
        assert result["session_type"] == "exam"
        assert result["wrong_count"] == 1
        assert result["wrong_answers"][0]["your_answer"] == "D"
        assert result["wrong_answers"][0]["correct_answer"] == "A"

    async def test_no_wrong_answers(self, db):
        from cert_pepper.db.connection import get_session
        from cert_pepper.mcp.study_engine import get_session_wrong_answers

        async with get_session() as session:
            user_id = await get_user_id(session)
            q1_id = await seed_question(session, number=1, correct_answer="A")

            await session.execute(
                text(
                    "INSERT INTO study_sessions (user_id, session_type, ended_at,"
                    " questions_seen, questions_correct)"
                    " VALUES (:uid, 'study', CURRENT_TIMESTAMP, 1, 1)"
                ),
                {"uid": user_id},
            )
            result = await session.execute(text("SELECT last_insert_rowid()"))
            sess_id = result.scalar()

            await session.execute(
                text(
                    "INSERT INTO question_attempts"
                    " (session_id, user_id, question_id, selected_answer, is_correct)"
                    " VALUES (:sid, :uid, :qid, 'A', 1)"
                ),
                {"sid": sess_id, "uid": user_id, "qid": q1_id},
            )

        result = json.loads(await get_session_wrong_answers())
        assert result["wrong_count"] == 0
        assert result["wrong_answers"] == []

    async def test_hint_references_get_explanation(self, db):
        from cert_pepper.db.connection import get_session
        from cert_pepper.mcp.study_engine import get_session_wrong_answers

        async with get_session() as session:
            user_id = await get_user_id(session)
            q1_id = await seed_question(session, number=1, correct_answer="B")

            await session.execute(
                text(
                    "INSERT INTO study_sessions (user_id, session_type, ended_at,"
                    " questions_seen, questions_correct)"
                    " VALUES (:uid, 'study', CURRENT_TIMESTAMP, 1, 0)"
                ),
                {"uid": user_id},
            )
            result = await session.execute(text("SELECT last_insert_rowid()"))
            sess_id = result.scalar()

            await session.execute(
                text(
                    "INSERT INTO question_attempts"
                    " (session_id, user_id, question_id, selected_answer, is_correct)"
                    " VALUES (:sid, :uid, :qid, 'A', 0)"
                ),
                {"sid": sess_id, "uid": user_id, "qid": q1_id},
            )

        result = json.loads(await get_session_wrong_answers())
        wrong = result["wrong_answers"]
        assert len(wrong) == 1
        hint = wrong[0]["hint"]
        assert "get_explanation" in hint
        assert str(q1_id) in hint

    async def test_unknown_session_id_returns_error(self, db):
        from cert_pepper.mcp.study_engine import get_session_wrong_answers

        result = json.loads(await get_session_wrong_answers(session_id=99999))
        assert "error" in result

    async def test_wrong_answers_include_all_options(self, db):
        from cert_pepper.db.connection import get_session
        from cert_pepper.mcp.study_engine import get_session_wrong_answers

        async with get_session() as session:
            user_id = await get_user_id(session)
            q1_id = await seed_question(session, number=1, correct_answer="C")

            await session.execute(
                text(
                    "INSERT INTO study_sessions (user_id, session_type, ended_at,"
                    " questions_seen, questions_correct)"
                    " VALUES (:uid, 'study', CURRENT_TIMESTAMP, 1, 0)"
                ),
                {"uid": user_id},
            )
            result = await session.execute(text("SELECT last_insert_rowid()"))
            sess_id = result.scalar()

            await session.execute(
                text(
                    "INSERT INTO question_attempts"
                    " (session_id, user_id, question_id, selected_answer, is_correct)"
                    " VALUES (:sid, :uid, :qid, 'A', 0)"
                ),
                {"sid": sess_id, "uid": user_id, "qid": q1_id},
            )

        result = json.loads(await get_session_wrong_answers())
        wrong = result["wrong_answers"]
        assert len(wrong) == 1
        options = wrong[0]["options"]
        assert set(options.keys()) == {"A", "B", "C", "D"}
        assert "domain" in wrong[0]
