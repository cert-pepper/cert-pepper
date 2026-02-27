"""Tests for engine/selector.py.

Covers:
  - select_question: returns None when empty, returns unseen questions,
    prefers FSRS review/learning cards, respects domain_filter
  - select_exam_questions: proportional by weight, random shuffle, capped at total
"""

from __future__ import annotations

from datetime import datetime, timedelta

import pytest
from sqlalchemy import text

from cert_pepper.db.connection import get_session
from cert_pepper.engine.selector import select_question, select_exam_questions

from tests.conftest import seed_question, seed_session, get_user_id


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

async def register_fsrs_card(
    session,
    user_id: int,
    question_id: int,
    state: str,
    due_date: datetime,
) -> None:
    """Insert an fsrs_cards row for a question."""
    await session.execute(
        text("""
            INSERT INTO fsrs_cards
                (user_id, content_type, content_id, state, due_date,
                 stability, difficulty, retrievability)
            VALUES (:uid, 'question', :qid, :state, :due, 1.0, 5.0, 1.0)
        """),
        {"uid": user_id, "qid": question_id, "state": state, "due": due_date},
    )


# ---------------------------------------------------------------------------
# select_question
# ---------------------------------------------------------------------------

class TestSelectQuestion:
    async def test_returns_none_when_no_questions(self, db):
        async with get_session() as session:
            user_id = await get_user_id(session)
            result = await select_question(session, user_id)
        assert result is None

    async def test_returns_unseen_question_id(self, db):
        async with get_session() as session:
            user_id = await get_user_id(session)
            q_id = await seed_question(session, domain_number=4, number=1)
            await session.commit()

        async with get_session() as session:
            user_id = await get_user_id(session)
            result = await select_question(session, user_id)

        assert result == q_id

    async def test_prefers_overdue_review_over_unseen(self, db):
        now = datetime.utcnow()
        async with get_session() as session:
            user_id = await get_user_id(session)
            unseen_id = await seed_question(session, domain_number=1, number=1)
            review_id = await seed_question(session, domain_number=4, number=2)
            # Register review card as overdue
            await register_fsrs_card(
                session, user_id, review_id,
                state="review",
                due_date=now - timedelta(days=2),
            )
            await session.commit()

        async with get_session() as session:
            user_id = await get_user_id(session)
            result = await select_question(session, user_id, now=now)

        assert result == review_id

    async def test_prefers_due_learning_over_unseen(self, db):
        now = datetime.utcnow()
        async with get_session() as session:
            user_id = await get_user_id(session)
            _unseen_id = await seed_question(session, domain_number=1, number=1)
            learning_id = await seed_question(session, domain_number=2, number=2)
            await register_fsrs_card(
                session, user_id, learning_id,
                state="learning",
                due_date=now - timedelta(minutes=5),
            )
            await session.commit()

        async with get_session() as session:
            user_id = await get_user_id(session)
            result = await select_question(session, user_id, now=now)

        assert result == learning_id

    async def test_future_review_card_not_selected_before_unseen(self, db):
        now = datetime.utcnow()
        async with get_session() as session:
            user_id = await get_user_id(session)
            unseen_id = await seed_question(session, domain_number=4, number=1)
            future_review_id = await seed_question(session, domain_number=4, number=2)
            await register_fsrs_card(
                session, user_id, future_review_id,
                state="review",
                due_date=now + timedelta(days=5),  # not yet due
            )
            await session.commit()

        async with get_session() as session:
            user_id = await get_user_id(session)
            result = await select_question(session, user_id, now=now)

        # Future card is not due → falls through to unseen
        assert result == unseen_id

    async def test_domain_filter_restricts_to_domain(self, db):
        async with get_session() as session:
            user_id = await get_user_id(session)
            d1_id = await seed_question(session, domain_number=1, number=1)
            _d4_id = await seed_question(session, domain_number=4, number=1)
            await session.commit()

        async with get_session() as session:
            user_id = await get_user_id(session)
            result = await select_question(session, user_id, domain_filter=1)

        assert result == d1_id

    async def test_domain_filter_returns_none_when_no_match(self, db):
        async with get_session() as session:
            user_id = await get_user_id(session)
            await seed_question(session, domain_number=4, number=1)
            await session.commit()

        async with get_session() as session:
            user_id = await get_user_id(session)
            # Filter on domain 2, but only domain 4 has questions
            result = await select_question(session, user_id, domain_filter=2)

        assert result is None


# ---------------------------------------------------------------------------
# select_exam_questions
# ---------------------------------------------------------------------------

class TestSelectExamQuestions:
    async def test_empty_db_returns_empty_list(self, db):
        async with get_session() as session:
            user_id = await get_user_id(session)
            result = await select_exam_questions(session, user_id)
        assert result == []

    async def test_returns_list_of_ints(self, db):
        async with get_session() as session:
            user_id = await get_user_id(session)
            for domain in range(1, 6):
                for num in range(1, 4):
                    await seed_question(session, domain_number=domain, number=num)
            await session.commit()

        async with get_session() as session:
            user_id = await get_user_id(session)
            result = await select_exam_questions(session, user_id, total=10)

        assert isinstance(result, list)
        assert all(isinstance(qid, int) for qid in result)

    async def test_does_not_exceed_total(self, db):
        async with get_session() as session:
            user_id = await get_user_id(session)
            for domain in range(1, 6):
                for num in range(1, 6):
                    await seed_question(session, domain_number=domain, number=num)
            await session.commit()

        async with get_session() as session:
            user_id = await get_user_id(session)
            result = await select_exam_questions(session, user_id, total=10)

        assert len(result) <= 10

    async def test_all_returned_ids_exist_in_db(self, db):
        async with get_session() as session:
            user_id = await get_user_id(session)
            inserted_ids = set()
            for domain in range(1, 6):
                for num in range(1, 4):
                    qid = await seed_question(session, domain_number=domain, number=num)
                    inserted_ids.add(qid)
            await session.commit()

        async with get_session() as session:
            user_id = await get_user_id(session)
            result = await select_exam_questions(session, user_id, total=10)

        for qid in result:
            assert qid in inserted_ids

    async def test_no_duplicate_ids(self, db):
        async with get_session() as session:
            user_id = await get_user_id(session)
            for domain in range(1, 6):
                for num in range(1, 10):
                    await seed_question(session, domain_number=domain, number=num)
            await session.commit()

        async with get_session() as session:
            user_id = await get_user_id(session)
            result = await select_exam_questions(session, user_id, total=20)

        assert len(result) == len(set(result))
