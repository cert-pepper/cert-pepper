"""Tests for engine/scorer.py.

Covers:
  - get_domain_accuracies: empty when no attempts, correct values after attempts
  - predict_score: 0 score with no attempts, 900 with perfect accuracy
  - get_weak_areas: all domains listed when unattempted, filtering by threshold
  - get_recommendations: urgency levels, count cap at 5
"""

from __future__ import annotations

import math
import pytest
from sqlalchemy import text

from cert_pepper.db.connection import get_session
from cert_pepper.engine.scorer import (
    get_domain_accuracies,
    predict_score,
    get_weak_areas,
    get_recommendations,
    DOMAIN_WEIGHTS,
    WEAK_AREA_THRESHOLD,
)

from tests.conftest import seed_question, seed_attempt, seed_session, get_user_id


# ---------------------------------------------------------------------------
# get_domain_accuracies
# ---------------------------------------------------------------------------

class TestGetDomainAccuracies:
    async def test_no_attempts_returns_empty_dict(self, db):
        async with get_session() as session:
            user_id = await get_user_id(session)
            result = await get_domain_accuracies(session, user_id)
        assert result == {}

    async def test_one_correct_attempt(self, db):
        async with get_session() as session:
            user_id = await get_user_id(session)
            session_id = await seed_session(session, user_id)
            q_id = await seed_question(session, domain_number=4)
            await seed_attempt(session, user_id, q_id, session_id, is_correct=True)
            await session.commit()

        async with get_session() as session:
            user_id = await get_user_id(session)
            result = await get_domain_accuracies(session, user_id)

        assert 4 in result
        accuracy, count = result[4]
        assert accuracy == pytest.approx(1.0)
        assert count == 1

    async def test_mixed_attempts_correct_accuracy(self, db):
        async with get_session() as session:
            user_id = await get_user_id(session)
            session_id = await seed_session(session, user_id)
            # 2 questions in domain 2
            q1 = await seed_question(session, domain_number=2, number=1)
            q2 = await seed_question(session, domain_number=2, number=2)
            await seed_attempt(session, user_id, q1, session_id, is_correct=True)
            await seed_attempt(session, user_id, q2, session_id, is_correct=False)
            await session.commit()

        async with get_session() as session:
            user_id = await get_user_id(session)
            result = await get_domain_accuracies(session, user_id)

        accuracy, count = result[2]
        assert accuracy == pytest.approx(0.5)
        assert count == 2

    async def test_multiple_domains_tracked_separately(self, db):
        async with get_session() as session:
            user_id = await get_user_id(session)
            session_id = await seed_session(session, user_id)
            q1 = await seed_question(session, domain_number=1, number=1)
            q2 = await seed_question(session, domain_number=3, number=1)
            await seed_attempt(session, user_id, q1, session_id, is_correct=True)
            await seed_attempt(session, user_id, q2, session_id, is_correct=False)
            await session.commit()

        async with get_session() as session:
            user_id = await get_user_id(session)
            result = await get_domain_accuracies(session, user_id)

        assert result[1][0] == pytest.approx(1.0)
        assert result[3][0] == pytest.approx(0.0)


# ---------------------------------------------------------------------------
# predict_score
# ---------------------------------------------------------------------------

class TestPredictScore:
    async def test_no_attempts_gives_zero_score(self, db):
        async with get_session() as session:
            user_id = await get_user_id(session)
            score = await predict_score(session, user_id)
        assert score.predicted_score == 0
        assert score.pass_probability < 0.5

    async def test_all_correct_gives_900(self, db):
        async with get_session() as session:
            user_id = await get_user_id(session)
            session_id = await seed_session(session, user_id)
            for domain in range(1, 6):
                q = await seed_question(session, domain_number=domain, number=1)
                await seed_attempt(session, user_id, q, session_id, is_correct=True)
            await session.commit()

        async with get_session() as session:
            user_id = await get_user_id(session)
            score = await predict_score(session, user_id)

        assert score.predicted_score == 900
        assert score.pass_probability > 0.5

    async def test_pass_probability_above_half_when_score_above_750(self, db):
        # Seed enough correct answers in high-weight domains to exceed 750
        async with get_session() as session:
            user_id = await get_user_id(session)
            session_id = await seed_session(session, user_id)
            for domain in range(1, 6):
                q = await seed_question(session, domain_number=domain, number=1)
                await seed_attempt(session, user_id, q, session_id, is_correct=True)
            await session.commit()

        async with get_session() as session:
            user_id = await get_user_id(session)
            score = await predict_score(session, user_id)

        assert score.pass_probability > 0.5

    async def test_score_fields_reflect_per_domain_accuracy(self, db):
        async with get_session() as session:
            user_id = await get_user_id(session)
            session_id = await seed_session(session, user_id)
            q = await seed_question(session, domain_number=4, number=1)
            await seed_attempt(session, user_id, q, session_id, is_correct=True)
            await session.commit()

        async with get_session() as session:
            user_id = await get_user_id(session)
            score = await predict_score(session, user_id)

        assert score.d4_accuracy == pytest.approx(1.0)
        assert score.d1_accuracy == pytest.approx(0.0)


# ---------------------------------------------------------------------------
# get_weak_areas
# ---------------------------------------------------------------------------

class TestGetWeakAreas:
    async def test_no_attempts_returns_all_five_domains(self, db):
        async with get_session() as session:
            user_id = await get_user_id(session)
            weak = await get_weak_areas(session, user_id)
        assert len(weak) == 5
        domain_nums = {w.domain_number for w in weak}
        assert domain_nums == {1, 2, 3, 4, 5}

    async def test_domains_sorted_by_priority_score_descending(self, db):
        async with get_session() as session:
            user_id = await get_user_id(session)
            weak = await get_weak_areas(session, user_id)
        priorities = [w.priority_score for w in weak]
        assert priorities == sorted(priorities, reverse=True)

    async def test_domain_with_full_accuracy_excluded(self, db):
        async with get_session() as session:
            user_id = await get_user_id(session)
            session_id = await seed_session(session, user_id)
            q = await seed_question(session, domain_number=1, number=1)
            await seed_attempt(session, user_id, q, session_id, is_correct=True)
            await session.commit()

        async with get_session() as session:
            user_id = await get_user_id(session)
            weak = await get_weak_areas(session, user_id, threshold=WEAK_AREA_THRESHOLD)

        # Domain 1 should NOT appear — 100% accuracy is above threshold
        domain_nums = {w.domain_number for w in weak}
        assert 1 not in domain_nums

    async def test_domain_below_threshold_appears_in_weak_areas(self, db):
        async with get_session() as session:
            user_id = await get_user_id(session)
            session_id = await seed_session(session, user_id)
            # 0% accuracy in domain 4
            q = await seed_question(session, domain_number=4, number=1)
            await seed_attempt(session, user_id, q, session_id, is_correct=False)
            await session.commit()

        async with get_session() as session:
            user_id = await get_user_id(session)
            weak = await get_weak_areas(session, user_id)

        domain_nums = {w.domain_number for w in weak}
        assert 4 in domain_nums

    async def test_unattempted_domain_has_zero_accuracy(self, db):
        async with get_session() as session:
            user_id = await get_user_id(session)
            weak = await get_weak_areas(session, user_id)

        for w in weak:
            if w.attempts == 0:
                assert w.accuracy_pct == 0.0

    async def test_priority_score_matches_formula(self, db):
        """priority = weight_pct/100 * (1 - accuracy) for unattempted domains."""
        async with get_session() as session:
            user_id = await get_user_id(session)
            weak = await get_weak_areas(session, user_id)

        # For an unattempted domain: priority = weight/100
        domain4 = next(w for w in weak if w.domain_number == 4)
        assert domain4.priority_score == pytest.approx(0.28, abs=1e-6)


# ---------------------------------------------------------------------------
# get_recommendations
# ---------------------------------------------------------------------------

class TestGetRecommendations:
    async def test_no_attempts_returns_recommendations(self, db):
        async with get_session() as session:
            user_id = await get_user_id(session)
            recs = await get_recommendations(session, user_id)
        assert len(recs) > 0

    async def test_returns_at_most_five(self, db):
        async with get_session() as session:
            user_id = await get_user_id(session)
            recs = await get_recommendations(session, user_id)
        assert len(recs) <= 5

    async def test_unattempted_high_weight_domain_is_critical(self, db):
        """Domain 4 (28%) with 0 attempts should have urgency=critical."""
        async with get_session() as session:
            user_id = await get_user_id(session)
            recs = await get_recommendations(session, user_id)

        domain4_rec = next((r for r in recs if r.domain_number == 4), None)
        assert domain4_rec is not None
        assert domain4_rec.urgency == "critical"

    async def test_recommended_minutes_at_least_15(self, db):
        async with get_session() as session:
            user_id = await get_user_id(session)
            recs = await get_recommendations(session, user_id)

        for rec in recs:
            assert rec.suggested_minutes >= 15

    async def test_recommendation_has_reason(self, db):
        async with get_session() as session:
            user_id = await get_user_id(session)
            recs = await get_recommendations(session, user_id)

        for rec in recs:
            assert len(rec.reason) > 0

    async def test_low_accuracy_domain_urgency_is_critical(self, db):
        async with get_session() as session:
            user_id = await get_user_id(session)
            session_id = await seed_session(session, user_id)
            # 30% accuracy in domain 2 (below 0.5 threshold for critical)
            for i in range(10):
                q = await seed_question(session, domain_number=2, number=i + 1)
                await seed_attempt(
                    session, user_id, q, session_id,
                    is_correct=(i < 3)  # 3 correct, 7 wrong = 30%
                )
            await session.commit()

        async with get_session() as session:
            user_id = await get_user_id(session)
            recs = await get_recommendations(session, user_id)

        domain2_rec = next((r for r in recs if r.domain_number == 2), None)
        assert domain2_rec is not None
        assert domain2_rec.urgency == "critical"
