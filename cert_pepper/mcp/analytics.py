"""MCP Server 3: analytics — score prediction and weak area reports."""

from __future__ import annotations

import json

from mcp.server.fastmcp import FastMCP
from sqlalchemy.ext.asyncio import AsyncSession

from cert_pepper.db.connection import get_session, init_db

mcp = FastMCP("cert-pepper-analytics")


async def _get_user_id(session: AsyncSession) -> int:
    from sqlalchemy import text

    result = await session.execute(text("SELECT id FROM users WHERE username='default' LIMIT 1"))
    row = result.fetchone()
    return row[0] if row else 1


@mcp.tool()
async def predict_score(exam_code: str | None = None) -> str:
    """Calculate predicted exam score and pass probability based on your performance."""
    from cert_pepper.db.exams import resolve_cert_id
    from cert_pepper.engine.scorer import predict_score as _predict_score

    async with get_session() as db:
        user_id = await _get_user_id(db)
        try:
            cert_id = await resolve_cert_id(db, exam_code)
        except ValueError as e:
            return json.dumps({"error": str(e)})
        score = await _predict_score(db, user_id, cert_id=cert_id)

    domain_acc = {
        f"domain_{d}": f"{acc:.0%}"
        for d, acc in sorted(score.domain_accuracies.items())
    }

    return json.dumps({
        "predicted_score": score.predicted_score,
        "pass_probability": f"{score.pass_probability:.0%}",
        "passing_score": 750,
        "status": "PASS" if score.predicted_score >= 750 else "FAIL",
        "domain_accuracies": domain_acc,
        "weighted_accuracy": f"{score.weighted_accuracy:.0%}",
    })


@mcp.tool()
async def get_weak_areas(threshold: float = 0.70, exam_code: str | None = None) -> str:
    """Get domains below a given accuracy threshold (0.0-1.0)."""
    from cert_pepper.db.exams import resolve_cert_id
    from cert_pepper.engine.scorer import get_weak_areas as _get_weak_areas

    async with get_session() as db:
        user_id = await _get_user_id(db)
        try:
            cert_id = await resolve_cert_id(db, exam_code)
        except ValueError as e:
            return json.dumps({"error": str(e)})
        weak = await _get_weak_areas(db, user_id, threshold=threshold, cert_id=cert_id)

    return json.dumps({
        "weak_areas": [
            {
                "domain": w.domain_number,
                "name": w.domain_name,
                "accuracy": f"{w.accuracy_pct:.0%}",
                "weight": f"{w.weight_pct:.0f}%",
                "attempts": w.attempts,
                "priority": round(w.priority_score, 3),
            }
            for w in weak
        ],
        "threshold": f"{threshold:.0%}",
    })


@mcp.tool()
async def get_study_recommendations(
    days_remaining: int = 10,
    exam_code: str | None = None,
) -> str:
    """Get prioritized study recommendations based on weak areas and days remaining."""
    from datetime import date

    from cert_pepper.db.exams import resolve_cert_id
    from cert_pepper.db.goals import get_goal
    from cert_pepper.engine.scorer import get_recommendations

    async with get_session() as db:
        user_id = await _get_user_id(db)
        try:
            cert_id = await resolve_cert_id(db, exam_code)
        except ValueError as e:
            return json.dumps({"error": str(e)})

        # Auto-populate days_remaining from user_goals if set
        goal = await get_goal(db, user_id, cert_id)
        if goal is not None:
            days_remaining = max(0, (goal["exam_date"] - date.today()).days)

        recs = await get_recommendations(
            db, user_id, days_remaining=days_remaining, cert_id=cert_id
        )

    return json.dumps({
        "days_remaining": days_remaining,
        "recommendations": [
            {
                "domain": r.domain_number,
                "name": r.domain_name,
                "urgency": r.urgency,
                "reason": r.reason,
                "suggested_minutes": r.suggested_minutes,
            }
            for r in recs
        ],
    })


@mcp.tool()
async def get_schedule_status(exam_code: str | None = None) -> str:
    """Return current schedule adherence and pace toward exam date.

    Returns JSON with: exam_date, days_remaining, target_hours, hours_completed,
    pct_complete, sessions_per_day, on_pace, missed_days_count.
    Requires a goal to be set via `cert-pepper goal set`.
    """
    from datetime import date

    from cert_pepper.db.exams import resolve_cert_id
    from cert_pepper.db.goals import (
        get_daily_session_counts,
        get_goal,
        get_hours_completed,
        get_sessions_today,
    )
    from cert_pepper.engine.scorer import compute_schedule_status, get_day_statuses

    async with get_session() as db:
        user_id = await _get_user_id(db)
        try:
            cert_id = await resolve_cert_id(db, exam_code)
        except ValueError as e:
            return json.dumps({"error": str(e)})

        goal = await get_goal(db, user_id, cert_id)
        if goal is None:
            return json.dumps({
                "error": "No goal set. Run: cert-pepper goal set --exam-date YYYY-MM-DD"
            })

        hours_completed = await get_hours_completed(db, user_id, cert_id)
        sessions_today = await get_sessions_today(db, user_id, cert_id)
        daily_counts = await get_daily_session_counts(db, user_id, cert_id)

    exam_date = goal["exam_date"]
    target_hours = goal["target_hours"]

    created_raw = goal.get("created_at")
    start_date = None
    if created_raw:
        try:
            start_date = date.fromisoformat(str(created_raw)[:10])
        except ValueError:
            pass

    status = compute_schedule_status(
        exam_date=exam_date,
        target_hours=target_hours,
        hours_completed=hours_completed,
        sessions_today=sessions_today,
        start_date=start_date,
    )

    # Count missed days
    from datetime import timedelta
    calendar_start = date.today() - timedelta(weeks=4)
    day_statuses = get_day_statuses(
        daily_sessions=daily_counts,
        exam_date=exam_date,
        sessions_per_day=status.sessions_per_day,
        start_date=calendar_start,
    )
    missed_days = sum(1 for ds in day_statuses if ds.status == "missed")

    return json.dumps({
        "exam_date": exam_date.isoformat(),
        "days_remaining": status.days_remaining,
        "target_hours": target_hours,
        "hours_completed": round(hours_completed, 2),
        "pct_complete": f"{status.pct_complete:.0%}",
        "sessions_per_day": status.sessions_per_day,
        "sessions_today": sessions_today,
        "on_pace": status.on_pace,
        "missed_days_count": missed_days,
    })


@mcp.tool()
async def get_performance_trend(days: int = 7, exam_code: str | None = None) -> str:
    """Get accuracy trend per domain over recent sessions."""
    from sqlalchemy import text

    async with get_session() as db:
        user_id = await _get_user_id(db)

        if exam_code:
            result = await db.execute(
                text("""
                    SELECT date(qa.created_at) as day,
                           d.number as domain_num,
                           COUNT(*) as total,
                           SUM(qa.is_correct) as correct
                    FROM question_attempts qa
                    JOIN questions q ON q.id = qa.question_id
                    JOIN domains d ON d.id = q.domain_id
                    JOIN certifications c ON c.id = d.certification_id AND c.code = :exam_code
                    WHERE qa.user_id = :uid
                    AND qa.created_at >= datetime('now', :days_ago)
                    GROUP BY day, domain_num
                    ORDER BY day DESC, domain_num
                """),
                {"uid": user_id, "days_ago": f"-{days} days", "exam_code": exam_code},
            )
        else:
            result = await db.execute(
                text("""
                    SELECT date(qa.created_at) as day,
                           d.number as domain_num,
                           COUNT(*) as total,
                           SUM(qa.is_correct) as correct
                    FROM question_attempts qa
                    JOIN questions q ON q.id = qa.question_id
                    JOIN domains d ON d.id = q.domain_id
                    WHERE qa.user_id = :uid
                    AND qa.created_at >= datetime('now', :days_ago)
                    GROUP BY day, domain_num
                    ORDER BY day DESC, domain_num
                """),
                {"uid": user_id, "days_ago": f"-{days} days"},
            )
        rows = result.fetchall()

    trend: dict[str, dict[str, str]] = {}
    for row in rows:
        day, domain_num, total, correct = row
        correct = correct or 0
        if day not in trend:
            trend[day] = {}
        trend[day][f"domain_{domain_num}"] = f"{(correct / total):.0%}" if total > 0 else "—"

    return json.dumps({"days": days, "trend": trend})


@mcp.resource("analytics://dashboard")
async def progress_dashboard() -> str:
    """Full progress report in Markdown."""
    from sqlalchemy import text

    from cert_pepper.db.exams import resolve_cert_id
    from cert_pepper.engine.scorer import get_weak_areas, predict_score

    async with get_session() as db:
        user_id = await _get_user_id(db)
        try:
            cert_id = await resolve_cert_id(db)
        except ValueError:
            cert_id = None

        score = await predict_score(db, user_id, cert_id=cert_id)
        weak = await get_weak_areas(db, user_id, cert_id=cert_id)

        result = await db.execute(
            text("SELECT COUNT(*), SUM(is_correct) FROM question_attempts WHERE user_id=:uid"),
            {"uid": user_id},
        )
        row = result.fetchone()
        assert row is not None
        total = row[0] or 0
        correct = row[1] or 0

        # Get domain names dynamically
        if cert_id is not None:
            result = await db.execute(
                text(
                    "SELECT number, name, weight_pct FROM domains"
                    " WHERE certification_id = :cid ORDER BY number"
                ),
                {"cid": cert_id},
            )
            domains = result.fetchall()
        else:
            domains = []

    acc = correct / total if total > 0 else 0
    status = "PASS READY" if score.predicted_score >= 750 else "NEEDS WORK"

    domain_rows = "\n".join(
        f"| D{num}: {name[:30]} | {score.domain_accuracies.get(num, 0.0):.0%} | {weight:.0f}% |"
        for num, name, weight in domains
    )

    report = f"""# cert-pepper Progress Dashboard

## Overview
- **Total Questions**: {total:,}
- **Overall Accuracy**: {acc:.0%}
- **Predicted Score**: {score.predicted_score}/900 ({status})
- **Pass Probability**: {score.pass_probability:.0%}

## Domain Accuracies
| Domain | Accuracy | Weight |
|--------|----------|--------|
{domain_rows}

## Weak Areas (below 70%)
{chr(10).join(
    f"- Domain {w.domain_number}: {w.domain_name} — {w.accuracy_pct:.0%} ({w.attempts} attempts)"
    for w in weak
) or "None — all domains above threshold!"}
"""
    return report


@mcp.resource("analytics://score-history")
async def score_history() -> str:
    """Predicted score over time."""
    from sqlalchemy import text

    async with get_session() as db:
        user_id = await _get_user_id(db)
        result = await db.execute(
            text("""
                SELECT created_at, predicted_score, pass_probability
                FROM predicted_scores WHERE user_id=:uid
                ORDER BY created_at DESC LIMIT 30
            """),
            {"uid": user_id},
        )
        rows = result.fetchall()

    data = [{"date": str(r[0]), "score": r[1], "pass_prob": f"{r[2]:.0%}"} for r in rows]
    return json.dumps(data)


def serve() -> None:
    """Entry point for the analytics MCP server (stdio transport)."""
    import asyncio

    asyncio.run(init_db())
    mcp.run(transport="stdio")


if __name__ == "__main__":
    serve()
