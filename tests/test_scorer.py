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
from datetime import date, timedelta

from cert_pepper.engine.scorer import (
    compute_streak,
    compute_schedule_status,
    get_day_statuses,
    get_domain_accuracies,
    get_question_counts,
    pepper_score,
    predict_score,
    get_weak_areas,
    get_recommendations,
    WEAK_AREA_THRESHOLD,
)

from tests.conftest import (
    seed_certification, seed_domains_for_cert, get_cert_id,
    seed_question, seed_attempt, seed_session, get_user_id,
)


# ---------------------------------------------------------------------------
# compute_streak
# ---------------------------------------------------------------------------

class TestComputeStreak:
    def test_empty_returns_zero(self):
        assert compute_streak([]) == 0

    def test_studied_today_only(self):
        assert compute_streak([date.today()]) == 1

    def test_studied_yesterday_only(self):
        assert compute_streak([date.today() - timedelta(days=1)]) == 1

    def test_two_days_ago_only_returns_zero(self):
        assert compute_streak([date.today() - timedelta(days=2)]) == 0

    def test_consecutive_from_today(self):
        today = date.today()
        assert compute_streak([today - timedelta(days=i) for i in range(5)]) == 5

    def test_consecutive_from_yesterday(self):
        yesterday = date.today() - timedelta(days=1)
        assert compute_streak([yesterday - timedelta(days=i) for i in range(4)]) == 4

    def test_gap_breaks_streak(self):
        today = date.today()
        assert compute_streak([today, today - timedelta(days=3)]) == 1

    def test_long_streak(self):
        today = date.today()
        assert compute_streak([today - timedelta(days=i) for i in range(100)]) == 100


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


# ---------------------------------------------------------------------------
# get_question_counts
# ---------------------------------------------------------------------------

class TestGetQuestionCounts:
    async def test_no_questions_all_zeros(self, db):
        async with get_session() as session:
            user_id = await get_user_id(session)
            counts = await get_question_counts(session, user_id)
        assert counts.new == 0
        assert counts.correct == 0
        assert counts.incorrect == 0
        assert counts.total == 0

    async def test_unattempted_question_is_new(self, db):
        async with get_session() as session:
            user_id = await get_user_id(session)
            await seed_question(session, domain_number=1, number=1)
            await session.commit()

        async with get_session() as session:
            user_id = await get_user_id(session)
            counts = await get_question_counts(session, user_id)
        assert counts.new == 1
        assert counts.correct == 0
        assert counts.incorrect == 0
        assert counts.total == 1

    async def test_correctly_answered_counted_as_correct(self, db):
        async with get_session() as session:
            user_id = await get_user_id(session)
            session_id = await seed_session(session, user_id)
            q = await seed_question(session, domain_number=1, number=1)
            await seed_attempt(session, user_id, q, session_id, is_correct=True)
            await session.commit()

        async with get_session() as session:
            user_id = await get_user_id(session)
            counts = await get_question_counts(session, user_id)
        assert counts.correct == 1
        assert counts.new == 0
        assert counts.incorrect == 0

    async def test_only_wrong_attempts_counted_as_incorrect(self, db):
        async with get_session() as session:
            user_id = await get_user_id(session)
            session_id = await seed_session(session, user_id)
            q = await seed_question(session, domain_number=1, number=1)
            await seed_attempt(session, user_id, q, session_id, is_correct=False)
            await session.commit()

        async with get_session() as session:
            user_id = await get_user_id(session)
            counts = await get_question_counts(session, user_id)
        assert counts.incorrect == 1
        assert counts.new == 0
        assert counts.correct == 0

    async def test_correct_after_wrong_is_correct_not_incorrect(self, db):
        async with get_session() as session:
            user_id = await get_user_id(session)
            session_id = await seed_session(session, user_id)
            q = await seed_question(session, domain_number=1, number=1)
            await seed_attempt(session, user_id, q, session_id, is_correct=False)
            await seed_attempt(session, user_id, q, session_id, is_correct=True)
            await session.commit()

        async with get_session() as session:
            user_id = await get_user_id(session)
            counts = await get_question_counts(session, user_id)
        assert counts.correct == 1
        assert counts.incorrect == 0
        assert counts.new == 0

    async def test_buckets_sum_to_total(self, db):
        async with get_session() as session:
            user_id = await get_user_id(session)
            session_id = await seed_session(session, user_id)
            # q1: new (no attempt)
            await seed_question(session, domain_number=1, number=1)
            # q2: correct
            q2 = await seed_question(session, domain_number=1, number=2)
            await seed_attempt(session, user_id, q2, session_id, is_correct=True)
            # q3: incorrect only
            q3 = await seed_question(session, domain_number=1, number=3)
            await seed_attempt(session, user_id, q3, session_id, is_correct=False)
            await session.commit()

        async with get_session() as session:
            user_id = await get_user_id(session)
            counts = await get_question_counts(session, user_id)
        assert counts.new == 1
        assert counts.correct == 1
        assert counts.incorrect == 1
        assert counts.total == 3
        assert counts.new + counts.correct + counts.incorrect == counts.total


# ---------------------------------------------------------------------------
# Multi-cert scoping
# ---------------------------------------------------------------------------

class TestMultiCertScoring:
    async def test_get_domain_accuracies_scoped_to_cert(self, db):
        """Attempts on cert B questions don't appear in cert A accuracy."""
        async with get_session() as session:
            user_id = await get_user_id(session)
            cert_a_id = await get_cert_id(session, "SY0-701")

            cert_b_id = await seed_certification(session, "CERT-SCORE-B")
            await seed_domains_for_cert(session, cert_b_id, [(1, "B Domain", 100.0)])

            sess_id = await seed_session(session, user_id)
            # Attempt on cert B question
            b_q = await seed_question(session, domain_number=1, cert_id=cert_b_id, number=999)
            await seed_attempt(session, user_id, b_q, sess_id, is_correct=True)
            await session.commit()

        async with get_session() as session:
            user_id = await get_user_id(session)
            cert_a_id = await get_cert_id(session, "SY0-701")
            result = await get_domain_accuracies(session, user_id, cert_id=cert_a_id)

        # Cert A should have no attempts recorded
        assert result == {}

    async def test_predict_score_reads_weights_from_db(self, db):
        """predict_score uses domain weights from the DB, not hardcoded constants."""
        async with get_session() as session:
            user_id = await get_user_id(session)
            cert_id = await get_cert_id(session, "SY0-701")
            sess_id = await seed_session(session, user_id)
            for domain in range(1, 6):
                q = await seed_question(session, domain_number=domain, number=1, cert_id=cert_id)
                await seed_attempt(session, user_id, q, sess_id, is_correct=True)
            await session.commit()

        async with get_session() as session:
            user_id = await get_user_id(session)
            cert_id = await get_cert_id(session, "SY0-701")
            score = await predict_score(session, user_id, cert_id=cert_id)

        # With all domains at 100%, score = 900
        assert score.predicted_score == 900
        assert set(score.domain_weights.keys()) == {1, 2, 3, 4, 5}

    async def test_get_weak_areas_scoped_to_cert(self, db):
        """get_weak_areas only returns domains from the specified cert."""
        async with get_session() as session:
            user_id = await get_user_id(session)
            cert_b_id = await seed_certification(session, "CERT-WEAK-B")
            await seed_domains_for_cert(session, cert_b_id, [(1, "B Domain", 100.0)])
            cert_b_q = await seed_question(session, domain_number=1, cert_id=cert_b_id, number=888)
            await session.commit()

        async with get_session() as session:
            user_id = await get_user_id(session)
            cert_a_id = await get_cert_id(session, "SY0-701")
            weak = await get_weak_areas(session, user_id, cert_id=cert_a_id)

        # Cert A has 5 domains; none of them is cert B's domain
        assert all(w.domain_number in {1, 2, 3, 4, 5} for w in weak)
        assert len(weak) == 5


# ---------------------------------------------------------------------------
# compute_schedule_status (pure function)
# ---------------------------------------------------------------------------

class TestScheduleStatus:
    def _exam(self, days_from_now: int = 6) -> date:
        return date.today() + timedelta(days=days_from_now)

    def _start(self, days_ago: int = 4) -> date:
        return date.today() - timedelta(days=days_ago)

    def test_basic_fields_computed(self):
        status = compute_schedule_status(
            exam_date=self._exam(6),
            target_hours=40,
            hours_completed=12.0,
            sessions_today=1,
            start_date=self._start(4),
        )
        assert status.exam_date == self._exam(6)
        assert status.target_hours == 40
        assert status.hours_completed == pytest.approx(12.0)
        assert status.hours_remaining == pytest.approx(28.0)
        assert status.days_remaining == 6
        assert status.sessions_today == 1
        assert 0.0 <= status.pct_complete <= 1.0

    def test_pct_complete_calculation(self):
        status = compute_schedule_status(
            exam_date=self._exam(10),
            target_hours=40,
            hours_completed=10.0,
            sessions_today=0,
            start_date=self._start(0),
        )
        assert status.pct_complete == pytest.approx(0.25)

    def test_sessions_per_day_typical(self):
        # 28h remaining, 6 days → 4.67h/day → ceil(4.67*60/45)=ceil(6.22)=7 → capped at 3
        status = compute_schedule_status(
            exam_date=self._exam(6),
            target_hours=40,
            hours_completed=12.0,
            sessions_today=0,
            start_date=self._start(4),
        )
        assert status.sessions_per_day == 3

    def test_sessions_per_day_minimum_one(self):
        # hours_remaining = 0 → sessions_per_day = 1 (minimum)
        status = compute_schedule_status(
            exam_date=self._exam(10),
            target_hours=40,
            hours_completed=40.0,
            sessions_today=0,
            start_date=self._start(4),
        )
        assert status.sessions_per_day == 1

    def test_sessions_per_day_capped_at_three(self):
        # Extreme: 39h remaining, 1 day → way over cap
        status = compute_schedule_status(
            exam_date=self._exam(1),
            target_hours=40,
            hours_completed=1.0,
            sessions_today=0,
            start_date=self._start(4),
        )
        assert status.sessions_per_day == 3

    def test_sessions_per_day_two(self):
        # 1.5h/day → ceil(1.5*60/45) = ceil(2.0) = 2
        status = compute_schedule_status(
            exam_date=self._exam(4),
            target_hours=10,
            hours_completed=4.0,
            sessions_today=0,
            start_date=self._start(4),
        )
        # 6h remaining / 4 days = 1.5h/day → 2 sessions
        assert status.sessions_per_day == 2

    def test_on_pace_when_ahead(self):
        # total_days=10, target=40h → planned=4h/day
        # hours_remaining=20, days_remaining=6 → required=3.33h/day ≤ 4 → on_pace=True
        status = compute_schedule_status(
            exam_date=self._exam(6),
            target_hours=40,
            hours_completed=20.0,
            sessions_today=0,
            start_date=self._start(4),
        )
        assert status.on_pace is True

    def test_not_on_pace_when_behind(self):
        # total_days=10, target=40h → planned=4h/day
        # hours_remaining=38, days_remaining=6 → required=6.33h/day > 4 → on_pace=False
        status = compute_schedule_status(
            exam_date=self._exam(6),
            target_hours=40,
            hours_completed=2.0,
            sessions_today=0,
            start_date=self._start(4),
        )
        assert status.on_pace is False

    def test_zero_days_remaining_no_crash(self):
        status = compute_schedule_status(
            exam_date=date.today(),
            target_hours=40,
            hours_completed=30.0,
            sessions_today=2,
            start_date=self._start(10),
        )
        assert status.days_remaining == 0
        assert status.sessions_per_day >= 1


# ---------------------------------------------------------------------------
# get_day_statuses (pure function)
# ---------------------------------------------------------------------------

class TestGetDayStatuses:
    def test_all_future_when_no_sessions(self):
        today = date.today()
        start = today + timedelta(days=1)
        exam = today + timedelta(days=7)
        statuses = get_day_statuses(
            daily_sessions={},
            exam_date=exam,
            sessions_per_day=2,
            start_date=start,
        )
        assert all(s.status == "future" for s in statuses)

    def test_met_day_when_sessions_at_or_above_target(self):
        today = date.today()
        past_day = today - timedelta(days=1)
        statuses = get_day_statuses(
            daily_sessions={past_day: 2},
            exam_date=today + timedelta(days=5),
            sessions_per_day=2,
            start_date=past_day,
        )
        day = next(s for s in statuses if s.date == past_day)
        assert day.status == "met"
        assert day.sessions_actual == 2

    def test_partial_day_when_some_but_below_target(self):
        today = date.today()
        past_day = today - timedelta(days=2)
        statuses = get_day_statuses(
            daily_sessions={past_day: 1},
            exam_date=today + timedelta(days=5),
            sessions_per_day=2,
            start_date=past_day,
        )
        day = next(s for s in statuses if s.date == past_day)
        assert day.status == "partial"

    def test_missed_day_when_zero_sessions_in_past(self):
        today = date.today()
        past_day = today - timedelta(days=3)
        statuses = get_day_statuses(
            daily_sessions={},
            exam_date=today + timedelta(days=5),
            sessions_per_day=2,
            start_date=past_day,
        )
        day = next(s for s in statuses if s.date == past_day)
        assert day.status == "missed"
        assert day.sessions_actual == 0

    def test_today_status(self):
        today = date.today()
        past = today - timedelta(days=1)
        statuses = get_day_statuses(
            daily_sessions={},
            exam_date=today + timedelta(days=5),
            sessions_per_day=2,
            start_date=past,
        )
        today_status = next(s for s in statuses if s.date == today)
        assert today_status.status == "today"

    def test_future_status(self):
        today = date.today()
        future = today + timedelta(days=3)
        statuses = get_day_statuses(
            daily_sessions={},
            exam_date=today + timedelta(days=7),
            sessions_per_day=2,
            start_date=today,
        )
        fut = next(s for s in statuses if s.date == future)
        assert fut.status == "future"

    def test_sessions_target_matches_sessions_per_day(self):
        today = date.today()
        start = today - timedelta(days=1)
        statuses = get_day_statuses(
            daily_sessions={},
            exam_date=today + timedelta(days=3),
            sessions_per_day=3,
            start_date=start,
        )
        assert all(s.sessions_target == 3 for s in statuses)

    def test_day_count_includes_exam_date(self):
        today = date.today()
        start = today
        exam = today + timedelta(days=4)
        statuses = get_day_statuses(
            daily_sessions={},
            exam_date=exam,
            sessions_per_day=1,
            start_date=start,
        )
        # should include start, start+1, ..., exam → 5 days
        assert len(statuses) == 5


# ---------------------------------------------------------------------------
# TestCoverageAdjustedScore
# ---------------------------------------------------------------------------

class TestCoverageAdjustedScore:
    async def test_unseen_questions_pull_score_toward_midpoint(self, db):
        """Extra unseen questions in domain 4 reduce effective accuracy below 1.0."""
        async with get_session() as session:
            user_id = await get_user_id(session)
            session_id = await seed_session(session, user_id)
            # Seed 1 question per domain, answer all correctly
            for domain in range(1, 6):
                q = await seed_question(session, domain_number=domain, number=1)
                await seed_attempt(session, user_id, q, session_id, is_correct=True)
            # Seed 4 more unanswered questions in domain 4
            for i in range(2, 6):
                await seed_question(session, domain_number=4, number=i)
            await session.commit()

        async with get_session() as session:
            user_id = await get_user_id(session)
            score = await predict_score(session, user_id)

        # Domain 4: seen=1, total=5, raw=1.0 → effective=(1.0+0.5*4)/5=0.6
        # Other domains: seen=total=1 → effective=1.0 → score must be < 900
        assert score.predicted_score < 900

    async def test_full_coverage_matches_raw_accuracy(self, db):
        """When all questions are answered, coverage-adjusted accuracy == raw accuracy."""
        async with get_session() as session:
            user_id = await get_user_id(session)
            session_id = await seed_session(session, user_id)
            q1 = await seed_question(session, domain_number=2, number=1)
            q2 = await seed_question(session, domain_number=2, number=2)
            await seed_attempt(session, user_id, q1, session_id, is_correct=True)
            await seed_attempt(session, user_id, q2, session_id, is_correct=False)
            await session.commit()

        async with get_session() as session:
            user_id = await get_user_id(session)
            score = await predict_score(session, user_id)

        # 1 correct, 1 wrong, 2 total → effective = (0.5*2 + 0.5*0) / 2 = 0.5
        # But seen == total → simplifies to raw = 0.5
        assert score.domain_accuracies[2] == pytest.approx(0.5)

    async def test_zero_coverage_gives_zero_score(self, db):
        """No questions seeded → total=0 per domain → predicted_score=0 (edge case)."""
        async with get_session() as session:
            user_id = await get_user_id(session)
            score = await predict_score(session, user_id)

        assert score.predicted_score == 0
        assert score.coverage_pct == pytest.approx(0.0)

    async def test_coverage_pct_field_is_correct(self, db):
        """coverage_pct = seen_distinct / total across all domains."""
        async with get_session() as session:
            user_id = await get_user_id(session)
            session_id = await seed_session(session, user_id)
            q1 = await seed_question(session, domain_number=1, number=1)
            await seed_question(session, domain_number=1, number=2)  # unanswered
            await seed_attempt(session, user_id, q1, session_id, is_correct=True)
            await session.commit()

        async with get_session() as session:
            user_id = await get_user_id(session)
            score = await predict_score(session, user_id)

        # 1 seen, 2 total → coverage = 0.5
        assert score.coverage_pct == pytest.approx(0.5)

    async def test_partial_coverage_score_below_full_accuracy_score(self, db):
        """Leaving questions unseen reduces predicted score even with 100% raw accuracy."""
        async with get_session() as session:
            user_id = await get_user_id(session)
            session_id = await seed_session(session, user_id)
            # Domain 1: 2 questions, answer only 1 correctly, leave 1 unseen
            q1 = await seed_question(session, domain_number=1, number=1)
            await seed_question(session, domain_number=1, number=2)  # unseen
            await seed_attempt(session, user_id, q1, session_id, is_correct=True)
            await session.commit()

        async with get_session() as session:
            user_id = await get_user_id(session)
            score = await predict_score(session, user_id)

        # effective_acc[1] = (1.0 * 1 + 0.5 * 1) / 2 = 0.75
        assert score.domain_accuracies[1] == pytest.approx(0.75)


# ---------------------------------------------------------------------------
# pepper_score (pure function)
# ---------------------------------------------------------------------------

class TestPepperScore:
    def test_returns_tuple_of_int_str(self):
        result = pepper_score(0.5)
        assert isinstance(result, tuple)
        assert len(result) == 2
        level, name = result
        assert isinstance(level, int)
        assert isinstance(name, str)

    def test_zero_percent_returns_bell_pepper(self):
        level, name = pepper_score(0.0)
        assert level == 1
        assert name == "Bell Pepper"

    def test_hundred_percent_returns_carolina_reaper(self):
        level, name = pepper_score(1.0)
        assert level == 10
        assert name == "Carolina Reaper"

    def test_ten_percent_boundary_is_banana_pepper(self):
        level, name = pepper_score(0.10)
        assert level == 2
        assert name == "Banana Pepper"

    def test_fifty_percent_is_serrano(self):
        level, name = pepper_score(0.50)
        assert level == 6
        assert name == "Cayenne"

    def test_ninety_percent_boundary(self):
        level, name = pepper_score(0.90)
        assert level == 10
        assert name == "Carolina Reaper"

    def test_just_below_ten_percent_is_bell_pepper(self):
        level, name = pepper_score(0.099)
        assert level == 1
        assert name == "Bell Pepper"

    def test_negative_clamps_to_level_one(self):
        level, name = pepper_score(-0.5)
        assert level == 1
        assert name == "Bell Pepper"

    def test_above_one_clamps_to_level_ten(self):
        level, name = pepper_score(1.5)
        assert level == 10
        assert name == "Carolina Reaper"

    def test_mid_range_levels(self):
        # 35% → level 4 (Jalapeño)
        level, name = pepper_score(0.35)
        assert level == 4
        assert name == "Jalapeño"

    def test_habanero_at_seventy_five(self):
        level, name = pepper_score(0.75)
        assert level == 8
        assert name == "Habanero"

    def test_ghost_pepper_at_eighty_five(self):
        level, name = pepper_score(0.85)
        assert level == 9
        assert name == "Ghost Pepper"


# ---------------------------------------------------------------------------
# TestPredictScorePassingScorePerCert
# ---------------------------------------------------------------------------

class TestPredictScorePassingScorePerCert:
    async def test_pass_probability_uses_cert_passing_score(self, db):
        """predict_score sigmoid must center on cert's passing_score, not 750.

        Two certs, identical accuracy → same predicted_score (~675).
        Cert with passing_score=600 → pass_prob > 0.5.
        Cert with passing_score=750 → pass_prob < 0.5.
        """
        from cert_pepper.db.connection import get_session
        from cert_pepper.engine.scorer import predict_score
        from sqlalchemy import text

        async def _seed_cert(session, code, passing_score):
            await session.execute(
                text(
                    "INSERT OR IGNORE INTO certifications "
                    "(code, name, vendor, passing_score, max_score) "
                    "VALUES (:code, :code, 'X', :ps, 900)"
                ),
                {"code": code, "ps": passing_score},
            )
            result = await session.execute(
                text("SELECT id FROM certifications WHERE code=:code"), {"code": code}
            )
            cert_id = result.scalar()
            await session.execute(
                text(
                    "INSERT INTO domains (certification_id, number, name, weight_pct) "
                    "VALUES (:cid, 1, 'D1', 100.0)"
                ),
                {"cid": cert_id},
            )
            result = await session.execute(
                text("SELECT id FROM domains WHERE certification_id=:cid AND number=1"),
                {"cid": cert_id},
            )
            domain_id = result.scalar()
            q_ids = []
            for i in range(4):
                result = await session.execute(
                    text(
                        "INSERT INTO questions "
                        "(domain_id, number, stem, option_a, option_b, option_c, option_d, "
                        "correct_answer, explanation) "
                        "VALUES (:did, :num, 'Q?', 'A', 'B', 'C', 'D', 'A', 'Exp') "
                        "RETURNING id"
                    ),
                    {"did": domain_id, "num": i + 1},
                )
                q_ids.append(result.scalar())
            return cert_id, q_ids

        async with get_session() as session:
            user_id = await get_user_id(session)
            cert_600_id, q600 = await _seed_cert(session, "CY0-TEST", 600)
            cert_750_id, q750 = await _seed_cert(session, "SY0-TEST", 750)
            sess_id = await seed_session(session, user_id)
            # 3 correct out of 4 seen → adjusted accuracy = 0.75 → predicted ≈ 675
            for i, qid in enumerate(q600):
                await seed_attempt(
                    session, session_id=sess_id, user_id=user_id,
                    question_id=qid, is_correct=1 if i < 3 else 0,
                )
            for i, qid in enumerate(q750):
                await seed_attempt(
                    session, session_id=sess_id, user_id=user_id,
                    question_id=qid, is_correct=1 if i < 3 else 0,
                )

        async with get_session() as session:
            score_600 = await predict_score(session, user_id=user_id, cert_id=cert_600_id)
            score_750 = await predict_score(session, user_id=user_id, cert_id=cert_750_id)

        # Same accuracy → same predicted score
        assert score_600.predicted_score == score_750.predicted_score

        # Lower threshold → higher pass probability at the same predicted score
        assert score_600.pass_probability > score_750.pass_probability, (
            f"600-passing cert should have higher pass_prob; "
            f"got 600-cert={score_600.pass_probability:.3f}, "
            f"750-cert={score_750.pass_probability:.3f}"
        )
        # At predicted ~675: above 600 threshold → pass_prob > 0.5
        assert score_600.pass_probability > 0.5
        # At predicted ~675: below 750 threshold → pass_prob < 0.5
        assert score_750.pass_probability < 0.5
