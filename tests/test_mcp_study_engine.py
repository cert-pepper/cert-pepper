"""Tests for get_session_wrong_answers MCP tool (TDD)."""

from __future__ import annotations

import json

import pytest
from sqlalchemy import text

from tests.conftest import get_user_id, seed_question


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
