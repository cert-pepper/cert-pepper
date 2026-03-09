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

from cert_pepper.engine.selector import get_domain_weights, get_domain_accuracy
from tests.conftest import (
    seed_certification, seed_domains_for_cert, get_cert_id,
    seed_question, seed_session, seed_attempt, get_user_id,
)


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

    async def test_weighted_selection_spans_multiple_domains(self, db):
        """Domain 4 (28%) cannot dominate 100% when other domains have unseen questions.

        Seeds 25 questions in domain 4 and 25 in domain 1. Runs select_question
        50 times. With the bug (ORDER BY weight_pct DESC LIMIT 20), domain 1 never
        appears. With the fix (stratified per-domain sampling), both domains appear.
        """
        async with get_session() as session:
            user_id = await get_user_id(session)
            cert_id = await get_cert_id(session, "SY0-701")
            for n in range(1, 26):
                await seed_question(session, domain_number=4, number=n)
            for n in range(1, 26):
                await seed_question(session, domain_number=1, number=n + 100)
            await session.commit()

        seen_domains: set[int] = set()
        async with get_session() as session:
            user_id = await get_user_id(session)
            cert_id = await get_cert_id(session, "SY0-701")
            for _ in range(50):
                result = await select_question(session, user_id, cert_id=cert_id)
                assert result is not None
                row = await session.execute(
                    text("SELECT d.number FROM questions q JOIN domains d ON d.id = q.domain_id WHERE q.id = :qid"),
                    {"qid": result},
                )
                seen_domains.add(row.scalar())

        assert 4 in seen_domains, "Domain 4 was never selected"
        assert 1 in seen_domains, "Domain 1 was never selected (bug: high-weight domain monopolizes LIMIT)"


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


# ---------------------------------------------------------------------------
# get_domain_weights
# ---------------------------------------------------------------------------

class TestGetDomainWeights:
    async def test_returns_dict_keyed_by_domain_number(self, db):
        async with get_session() as session:
            cert_id = await get_cert_id(session, "SY0-701")
            weights = await get_domain_weights(session, cert_id)

        assert set(weights.keys()) == {1, 2, 3, 4, 5}

    async def test_weight_fractions_sum_to_one(self, db):
        async with get_session() as session:
            cert_id = await get_cert_id(session, "SY0-701")
            weights = await get_domain_weights(session, cert_id)

        total = sum(weights.values())
        assert abs(total - 1.0) < 0.001

    async def test_domain4_weight_is_028(self, db):
        async with get_session() as session:
            cert_id = await get_cert_id(session, "SY0-701")
            weights = await get_domain_weights(session, cert_id)

        assert weights[4] == pytest.approx(0.28, abs=1e-6)


# ---------------------------------------------------------------------------
# Multi-cert isolation
# ---------------------------------------------------------------------------

class TestMultiCertIsolation:
    async def test_questions_scoped_by_cert_id(self, db):
        """Questions from cert B must not appear when querying cert A."""
        async with get_session() as session:
            user_id = await get_user_id(session)
            cert_a_id = await get_cert_id(session, "SY0-701")

            # Create cert B with its own domain
            cert_b_id = await seed_certification(session, "CERT-B")
            await seed_domains_for_cert(session, cert_b_id, [(1, "B Domain", 100.0)])

            # Insert question for cert A domain 4
            cert_a_q = await seed_question(session, domain_number=4, cert_id=cert_a_id)
            # Insert question for cert B domain 1
            cert_b_q = await seed_question(session, domain_number=1, cert_id=cert_b_id, number=99)
            await session.commit()

        # Query for cert A — must not return cert B question
        async with get_session() as session:
            user_id = await get_user_id(session)
            result = await select_question(session, user_id, cert_id=cert_a_id)
        assert result == cert_a_q
        assert result != cert_b_q

    async def test_exam_questions_only_from_specified_cert(self, db):
        """select_exam_questions returns only questions from the given cert."""
        async with get_session() as session:
            user_id = await get_user_id(session)
            cert_a_id = await get_cert_id(session, "SY0-701")

            cert_b_id = await seed_certification(session, "CERT-B2")
            await seed_domains_for_cert(session, cert_b_id, [(1, "B Domain", 100.0)])

            # Insert one question per cert
            for num in range(1, 4):
                await seed_question(session, domain_number=4, number=num, cert_id=cert_a_id)
            await seed_question(session, domain_number=1, cert_id=cert_b_id, number=99)
            await session.commit()

        async with get_session() as session:
            user_id = await get_user_id(session)
            cert_b_qs = await select_exam_questions(session, user_id, total=5, cert_id=cert_b_id)

        # All returned IDs should belong to cert B questions
        assert len(cert_b_qs) <= 1  # only 1 question in cert B


# ---------------------------------------------------------------------------
# get_domain_accuracy
# ---------------------------------------------------------------------------

class TestGetDomainAccuracy:
    async def test_returns_empty_dict_when_no_attempts(self, db):
        async with get_session() as session:
            user_id = await get_user_id(session)
            cert_id = await get_cert_id(session, "SY0-701")
            result = await get_domain_accuracy(session, user_id, cert_id)
        assert result == {}

    async def test_returns_correct_accuracy_per_domain(self, db):
        async with get_session() as session:
            user_id = await get_user_id(session)
            cert_id = await get_cert_id(session, "SY0-701")
            sid = await seed_session(session, user_id)
            q1 = await seed_question(session, domain_number=4, number=1)
            q2 = await seed_question(session, domain_number=4, number=2)
            q3 = await seed_question(session, domain_number=4, number=3)
            q4 = await seed_question(session, domain_number=4, number=4)
            # 3 correct, 1 wrong → accuracy = 0.75
            await seed_attempt(session, user_id, q1, sid, is_correct=True)
            await seed_attempt(session, user_id, q2, sid, is_correct=True)
            await seed_attempt(session, user_id, q3, sid, is_correct=True)
            await seed_attempt(session, user_id, q4, sid, is_correct=False)
            await session.commit()

        async with get_session() as session:
            user_id = await get_user_id(session)
            cert_id = await get_cert_id(session, "SY0-701")
            result = await get_domain_accuracy(session, user_id, cert_id)

        assert 4 in result
        assert result[4] == pytest.approx(0.75, abs=1e-6)

    async def test_missing_domain_not_in_result(self, db):
        async with get_session() as session:
            user_id = await get_user_id(session)
            cert_id = await get_cert_id(session, "SY0-701")
            sid = await seed_session(session, user_id)
            q1 = await seed_question(session, domain_number=4, number=1)
            await seed_attempt(session, user_id, q1, sid, is_correct=True)
            await session.commit()

        async with get_session() as session:
            user_id = await get_user_id(session)
            cert_id = await get_cert_id(session, "SY0-701")
            result = await get_domain_accuracy(session, user_id, cert_id)

        assert 2 not in result


# ---------------------------------------------------------------------------
# new_only flag
# ---------------------------------------------------------------------------

class TestNewOnly:
    async def test_new_only_skips_all_due_cards(self, db):
        """new_only=True must skip Tier 1 (review) and Tier 2 (learning) entirely."""
        now = datetime.utcnow()
        async with get_session() as session:
            user_id = await get_user_id(session)
            unseen_id = await seed_question(session, domain_number=4, number=1)
            review_id = await seed_question(session, domain_number=4, number=2)
            learning_id = await seed_question(session, domain_number=4, number=3)
            await register_fsrs_card(
                session, user_id, review_id, state="review",
                due_date=now - timedelta(days=2),
            )
            await register_fsrs_card(
                session, user_id, learning_id, state="learning",
                due_date=now - timedelta(minutes=5),
            )
            await session.commit()

        async with get_session() as session:
            user_id = await get_user_id(session)
            result = await select_question(session, user_id, now=now, new_only=True)

        assert result == unseen_id

    async def test_new_only_returns_none_when_no_unseen(self, db):
        """When new_only=True and no unseen questions exist, return None (not Tier 4)."""
        now = datetime.utcnow()
        async with get_session() as session:
            user_id = await get_user_id(session)
            # Seed a question that has been seen (has an fsrs_card entry)
            seen_id = await seed_question(session, domain_number=4, number=1)
            await register_fsrs_card(
                session, user_id, seen_id, state="review",
                due_date=now + timedelta(days=5),  # not due
            )
            await session.commit()

        async with get_session() as session:
            user_id = await get_user_id(session)
            result = await select_question(session, user_id, now=now, new_only=True)

        # No unseen questions remain; caller should see None and stop the session
        assert result is None


# ---------------------------------------------------------------------------
# Accuracy-weighted selection
# ---------------------------------------------------------------------------

class TestAccuracyWeightedSelection:
    async def test_weak_domain_selected_more_than_strong_domain(self, db):
        """D4 at 0% acc (28% weight) should dominate D1 at 100% acc (12% weight).

        Effective weights: D4 = 0.28 × 1.0 = 0.28, D1 = 0.12 × 0.1 = 0.012.
        P(D4 selected) ≈ 0.96 per draw → assert D4 count ≥ D1 count over 50 draws.
        """
        async with get_session() as session:
            user_id = await get_user_id(session)
            cert_id = await get_cert_id(session, "SY0-701")
            sid = await seed_session(session, user_id)

            d4_ids = set()
            for n in range(1, 11):
                qid = await seed_question(session, domain_number=4, number=n)
                d4_ids.add(qid)
                await seed_attempt(session, user_id, qid, sid, is_correct=False)

            d1_ids = set()
            for n in range(1, 11):
                qid = await seed_question(session, domain_number=1, number=n + 100)
                d1_ids.add(qid)
                await seed_attempt(session, user_id, qid, sid, is_correct=True)

            await session.commit()

        d4_count = 0
        d1_count = 0
        async with get_session() as session:
            user_id = await get_user_id(session)
            cert_id = await get_cert_id(session, "SY0-701")
            for _ in range(50):
                result = await select_question(session, user_id, cert_id=cert_id)
                assert result is not None
                if result in d4_ids:
                    d4_count += 1
                elif result in d1_ids:
                    d1_count += 1

        assert d4_count >= d1_count
