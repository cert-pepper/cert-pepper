"""Tests for FSRS-4.5 algorithm."""

from __future__ import annotations

from datetime import datetime, timedelta

import pytest

from cert_pepper.engine.fsrs import (
    FSRSCard,
    schedule,
    retrievability,
    initial_stability,
    initial_difficulty,
    next_interval,
    is_due,
    days_until_due,
    DECAY,
    FACTOR,
)


class TestRetrievability:
    def test_at_zero_days_is_one(self):
        assert retrievability(1.0, 0.0) == pytest.approx(1.0, abs=0.001)

    def test_decays_over_time(self):
        r1 = retrievability(10.0, 1.0)
        r2 = retrievability(10.0, 5.0)
        assert r1 > r2

    def test_higher_stability_slower_decay(self):
        r_low = retrievability(5.0, 10.0)
        r_high = retrievability(20.0, 10.0)
        assert r_high > r_low

    def test_negative_elapsed_returns_one(self):
        assert retrievability(1.0, -1.0) == pytest.approx(1.0, abs=0.001)


class TestInitialValues:
    def test_stability_increases_with_rating(self):
        s1 = initial_stability(1)
        s2 = initial_stability(2)
        s3 = initial_stability(3)
        s4 = initial_stability(4)
        assert s1 < s2 < s3 < s4

    def test_difficulty_decreases_with_rating(self):
        # Higher rating (easier) → lower difficulty value
        d1 = initial_difficulty(1)  # Again → hardest
        d4 = initial_difficulty(4)  # Easy → easiest
        assert d1 > d4

    def test_difficulty_clamped_to_1_10_scale(self):
        # Difficulty is on a 1-10 scale (FSRS spec)
        for rating in [1, 2, 3, 4]:
            d = initial_difficulty(rating)
            assert 1.0 <= d <= 10.0


class TestStateTransitions:
    def test_new_card_again_enters_learning(self):
        card = FSRSCard()
        now = datetime(2024, 1, 1, 12, 0)
        updated = schedule(card, 1, now)
        assert updated.state == "learning"
        assert updated.step == 0
        # Due in ~1 minute
        assert (updated.due_date - now).total_seconds() < 120

    def test_new_card_good_enters_learning_step1(self):
        card = FSRSCard()
        now = datetime(2024, 1, 1, 12, 0)
        updated = schedule(card, 3, now)
        assert updated.state == "learning"
        assert updated.step == 1

    def test_new_card_easy_graduates_to_review(self):
        card = FSRSCard()
        now = datetime(2024, 1, 1, 12, 0)
        updated = schedule(card, 4, now)
        assert updated.state == "review"
        assert updated.due_date > now + timedelta(hours=1)

    def test_learning_good_graduates_to_review(self):
        card = FSRSCard(state="learning", step=1, stability=1.0, difficulty=0.3)
        now = datetime(2024, 1, 1, 12, 0)
        updated = schedule(card, 3, now)
        assert updated.state == "review"

    def test_review_again_enters_relearning(self):
        card = FSRSCard(state="review", stability=10.0, difficulty=0.3, reps=5)
        now = datetime(2024, 1, 1, 12, 0)
        updated = schedule(card, 1, now)
        assert updated.state == "relearning"
        assert updated.lapses == 1

    def test_review_good_stays_review_longer_interval(self):
        card = FSRSCard(state="review", stability=10.0, difficulty=0.3, reps=5)
        now = datetime(2024, 1, 1, 12, 0)
        card.last_review = now - timedelta(days=10)
        updated = schedule(card, 3, now)
        assert updated.state == "review"
        # Interval should be >= 1 day
        interval_days = (updated.due_date - now).total_seconds() / 86400
        assert interval_days >= 1.0

    def test_relearning_good_returns_to_review(self):
        card = FSRSCard(state="relearning", step=0, stability=5.0, difficulty=0.5, lapses=1)
        now = datetime(2024, 1, 1, 12, 0)
        updated = schedule(card, 3, now)
        assert updated.state == "review"

    def test_reps_increment(self):
        card = FSRSCard()
        now = datetime(2024, 1, 1, 12, 0)
        updated = schedule(card, 3, now)
        assert updated.reps == 1


class TestInterval:
    def test_interval_at_least_one_day(self):
        assert next_interval(1.0) >= 1.0

    def test_higher_stability_longer_interval(self):
        i1 = next_interval(10.0)
        i2 = next_interval(50.0)
        assert i2 > i1

    def test_interval_grows_with_successive_good_reviews(self):
        card = FSRSCard()
        now = datetime(2024, 1, 1)
        intervals = []

        # Graduate
        card = schedule(card, 4, now)
        for i in range(5):
            review_date = card.due_date
            prev_due = card.due_date
            card = schedule(card, 3, review_date)
            interval = (card.due_date - review_date).total_seconds() / 86400
            intervals.append(interval)

        # Intervals should generally increase
        assert intervals[-1] > intervals[0]


class TestDueness:
    def test_new_card_is_due(self):
        card = FSRSCard()
        card.due_date = datetime.utcnow() - timedelta(seconds=1)
        assert is_due(card)

    def test_future_card_not_due(self):
        card = FSRSCard()
        card.due_date = datetime.utcnow() + timedelta(days=10)
        assert not is_due(card)

    def test_days_until_due_negative_when_overdue(self):
        card = FSRSCard()
        card.due_date = datetime.utcnow() - timedelta(days=2)
        assert days_until_due(card) < 0


class TestDifficultyUpdate:
    def test_again_increases_difficulty(self):
        from cert_pepper.engine.fsrs import next_difficulty
        d = 5.0   # midpoint on 1-10 scale
        d_after = next_difficulty(d, 1)  # Again
        assert d_after >= d  # Again should increase difficulty or keep it

    def test_easy_decreases_difficulty(self):
        from cert_pepper.engine.fsrs import next_difficulty
        d = 5.0   # midpoint on 1-10 scale
        d_after = next_difficulty(d, 4)  # Easy
        assert d_after <= d  # Easy should decrease difficulty

    def test_difficulty_clamped(self):
        from cert_pepper.engine.fsrs import next_difficulty
        # Test with values on the 1-10 scale
        for rating in [1, 2, 3, 4]:
            for d in [1.0, 5.0, 10.0]:
                d_new = next_difficulty(d, rating)
                assert 1.0 <= d_new <= 10.0
