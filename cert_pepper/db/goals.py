"""DB helpers for user study goals."""

from __future__ import annotations

from datetime import date

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


async def get_goal(
    session: AsyncSession,
    user_id: int,
    cert_id: int,
) -> dict | None:
    """Return the user's goal for a certification, or None if not set."""
    result = await session.execute(
        text("""
            SELECT exam_date, target_hours, created_at
            FROM user_goals
            WHERE user_id = :uid AND certification_id = :cid
        """),
        {"uid": user_id, "cid": cert_id},
    )
    row = result.fetchone()
    if row is None:
        return None
    return {
        "exam_date": date.fromisoformat(str(row[0])),
        "target_hours": row[1],
        "created_at": row[2],
    }


async def upsert_goal(
    session: AsyncSession,
    user_id: int,
    cert_id: int,
    exam_date: date,
    target_hours: int = 40,
) -> None:
    """Insert or update the user's exam goal."""
    await session.execute(
        text("""
            INSERT INTO user_goals (user_id, certification_id, exam_date, target_hours)
            VALUES (:uid, :cid, :exam_date, :hours)
            ON CONFLICT(user_id, certification_id) DO UPDATE SET
                exam_date = excluded.exam_date,
                target_hours = excluded.target_hours,
                updated_at = CURRENT_TIMESTAMP
        """),
        {
            "uid": user_id,
            "cid": cert_id,
            "exam_date": exam_date.isoformat(),
            "hours": target_hours,
        },
    )


async def get_hours_completed(
    session: AsyncSession,
    user_id: int,
    cert_id: int,
) -> float:
    """Return total hours studied (from study_sessions.total_time_seconds)."""
    result = await session.execute(
        text("""
            SELECT COALESCE(SUM(total_time_seconds), 0)
            FROM study_sessions
            WHERE user_id = :uid AND certification_id = :cid
        """),
        {"uid": user_id, "cid": cert_id},
    )
    row = result.fetchone()
    seconds = row[0] if row else 0
    return seconds / 3600.0


async def get_daily_session_counts(
    session: AsyncSession,
    user_id: int,
    cert_id: int,
) -> dict[date, int]:
    """Return {date: session_count} for all days with at least one session."""
    result = await session.execute(
        text("""
            SELECT DATE(started_at) as day, COUNT(*) as cnt
            FROM study_sessions
            WHERE user_id = :uid AND certification_id = :cid
            GROUP BY DATE(started_at)
        """),
        {"uid": user_id, "cid": cert_id},
    )
    return {
        date.fromisoformat(row[0]): row[1]
        for row in result.fetchall()
    }


async def get_sessions_today(
    session: AsyncSession,
    user_id: int,
    cert_id: int,
    today: date | None = None,
) -> int:
    """Return the number of study sessions started today."""
    if today is None:
        today = date.today()
    result = await session.execute(
        text("""
            SELECT COUNT(*)
            FROM study_sessions
            WHERE user_id = :uid
            AND certification_id = :cid
            AND DATE(started_at) = :today
        """),
        {"uid": user_id, "cid": cert_id, "today": today.isoformat()},
    )
    row = result.fetchone()
    return row[0] if row else 0
