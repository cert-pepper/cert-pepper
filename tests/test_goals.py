"""Tests for cert_pepper/db/goals.py DB helpers.

Covers: upsert_goal, get_goal, get_hours_completed,
        get_daily_session_counts, get_sessions_today.
"""

from __future__ import annotations

from datetime import date, timedelta

import pytest
from sqlalchemy import text

from cert_pepper.db.connection import get_session
from cert_pepper.db.goals import (
    get_daily_session_counts,
    get_goal,
    get_hours_completed,
    get_sessions_today,
    upsert_goal,
)

from tests.conftest import get_cert_id, get_user_id, seed_session


EXAM_DATE = date(2026, 3, 9)


class TestGoalDB:
    async def test_get_goal_returns_none_when_not_set(self, db):
        async with get_session() as session:
            user_id = await get_user_id(session)
            cert_id = await get_cert_id(session, "SY0-701")
            result = await get_goal(session, user_id, cert_id)
        assert result is None

    async def test_upsert_goal_and_get_goal(self, db):
        async with get_session() as session:
            user_id = await get_user_id(session)
            cert_id = await get_cert_id(session, "SY0-701")
            await upsert_goal(session, user_id, cert_id, EXAM_DATE, target_hours=40)
            await session.commit()

        async with get_session() as session:
            user_id = await get_user_id(session)
            cert_id = await get_cert_id(session, "SY0-701")
            goal = await get_goal(session, user_id, cert_id)

        assert goal is not None
        assert goal["exam_date"] == EXAM_DATE
        assert goal["target_hours"] == 40

    async def test_upsert_goal_updates_on_conflict(self, db):
        async with get_session() as session:
            user_id = await get_user_id(session)
            cert_id = await get_cert_id(session, "SY0-701")
            await upsert_goal(session, user_id, cert_id, EXAM_DATE, target_hours=40)
            await session.commit()

        new_date = date(2026, 4, 1)
        async with get_session() as session:
            user_id = await get_user_id(session)
            cert_id = await get_cert_id(session, "SY0-701")
            await upsert_goal(session, user_id, cert_id, new_date, target_hours=60)
            await session.commit()

        async with get_session() as session:
            user_id = await get_user_id(session)
            cert_id = await get_cert_id(session, "SY0-701")
            goal = await get_goal(session, user_id, cert_id)

        assert goal["exam_date"] == new_date
        assert goal["target_hours"] == 60

    async def test_get_hours_completed_zero_when_no_sessions(self, db):
        async with get_session() as session:
            user_id = await get_user_id(session)
            cert_id = await get_cert_id(session, "SY0-701")
            hours = await get_hours_completed(session, user_id, cert_id)
        assert hours == pytest.approx(0.0)

    async def test_get_hours_completed_sums_session_times(self, db):
        async with get_session() as session:
            user_id = await get_user_id(session)
            cert_id = await get_cert_id(session, "SY0-701")
            # Insert two sessions: 1800s + 900s = 2700s = 0.75h
            await session.execute(
                text("""
                    INSERT INTO study_sessions
                        (user_id, session_type, certification_id, total_time_seconds)
                    VALUES (:uid, 'study', :cid, 1800)
                """),
                {"uid": user_id, "cid": cert_id},
            )
            await session.execute(
                text("""
                    INSERT INTO study_sessions
                        (user_id, session_type, certification_id, total_time_seconds)
                    VALUES (:uid, 'study', :cid, 900)
                """),
                {"uid": user_id, "cid": cert_id},
            )
            await session.commit()

        async with get_session() as session:
            user_id = await get_user_id(session)
            cert_id = await get_cert_id(session, "SY0-701")
            hours = await get_hours_completed(session, user_id, cert_id)

        assert hours == pytest.approx(0.75)

    async def test_get_daily_session_counts_empty(self, db):
        async with get_session() as session:
            user_id = await get_user_id(session)
            cert_id = await get_cert_id(session, "SY0-701")
            counts = await get_daily_session_counts(session, user_id, cert_id)
        assert counts == {}

    async def test_get_daily_session_counts_groups_by_date(self, db):
        today = date.today()
        async with get_session() as session:
            user_id = await get_user_id(session)
            cert_id = await get_cert_id(session, "SY0-701")
            # Insert 2 sessions today, 1 yesterday
            for _ in range(2):
                await session.execute(
                    text("""
                        INSERT INTO study_sessions
                            (user_id, session_type, certification_id, started_at)
                        VALUES (:uid, 'study', :cid, :started)
                    """),
                    {"uid": user_id, "cid": cert_id, "started": f"{today.isoformat()} 12:00:00"},
                )
            yesterday = today - timedelta(days=1)
            await session.execute(
                text("""
                    INSERT INTO study_sessions
                        (user_id, session_type, certification_id, started_at)
                    VALUES (:uid, 'study', :cid, :started)
                """),
                {"uid": user_id, "cid": cert_id, "started": f"{yesterday.isoformat()} 12:00:00"},
            )
            await session.commit()

        async with get_session() as session:
            user_id = await get_user_id(session)
            cert_id = await get_cert_id(session, "SY0-701")
            counts = await get_daily_session_counts(session, user_id, cert_id)

        assert counts.get(today) == 2
        assert counts.get(yesterday) == 1

    async def test_get_sessions_today_zero_when_none(self, db):
        async with get_session() as session:
            user_id = await get_user_id(session)
            cert_id = await get_cert_id(session, "SY0-701")
            count = await get_sessions_today(session, user_id, cert_id)
        assert count == 0

    async def test_get_sessions_today_counts_todays_sessions(self, db):
        today = date.today()
        async with get_session() as session:
            user_id = await get_user_id(session)
            cert_id = await get_cert_id(session, "SY0-701")
            for _ in range(3):
                await session.execute(
                    text("""
                        INSERT INTO study_sessions
                            (user_id, session_type, certification_id, started_at)
                        VALUES (:uid, 'study', :cid, :started)
                    """),
                    {"uid": user_id, "cid": cert_id,
                     "started": f"{today.isoformat()} 12:00:00"},
                )
            # Yesterday session should NOT count
            yesterday = today - timedelta(days=1)
            await session.execute(
                text("""
                    INSERT INTO study_sessions
                        (user_id, session_type, certification_id, started_at)
                    VALUES (:uid, 'study', :cid, :started)
                """),
                {"uid": user_id, "cid": cert_id,
                 "started": f"{yesterday.isoformat()} 12:00:00"},
            )
            await session.commit()

        async with get_session() as session:
            user_id = await get_user_id(session)
            cert_id = await get_cert_id(session, "SY0-701")
            count = await get_sessions_today(session, user_id, cert_id)

        assert count == 3
