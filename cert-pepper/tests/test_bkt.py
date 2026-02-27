"""Tests for Bayesian Knowledge Tracing (BKT)."""

from __future__ import annotations

import pytest
from cert_pepper.engine.bkt import BKTParams, update, is_mastered, p_correct_next


class TestBKTUpdate:
    def test_correct_increases_mastery(self):
        params = BKTParams(p_mastery=0.3)
        updated = update(params, is_correct=True)
        assert updated.p_mastery > params.p_mastery

    def test_incorrect_decreases_mastery(self):
        params = BKTParams(p_mastery=0.8)
        updated = update(params, is_correct=False)
        assert updated.p_mastery < params.p_mastery

    def test_attempts_increment(self):
        params = BKTParams()
        updated = update(params, is_correct=True)
        assert updated.attempts == 1
        updated2 = update(updated, is_correct=False)
        assert updated2.attempts == 2

    def test_correct_increments_correct(self):
        params = BKTParams()
        updated = update(params, is_correct=True)
        assert updated.correct == 1

    def test_incorrect_does_not_increment_correct(self):
        params = BKTParams()
        updated = update(params, is_correct=False)
        assert updated.correct == 0

    def test_mastery_clamped_0_to_1(self):
        # Starting very high mastery and correct — should clamp at 1.0
        params = BKTParams(p_mastery=0.99, p_slip=0.01)
        updated = update(params, is_correct=True)
        assert 0.0 <= updated.p_mastery <= 1.0

    def test_mastery_converges_with_consecutive_correct(self):
        params = BKTParams(p_mastery=0.1)
        for _ in range(20):
            params = update(params, is_correct=True)
        assert params.p_mastery > 0.80

    def test_parameters_preserved(self):
        original = BKTParams(p_mastery=0.5, p_learn=0.25, p_guess=0.15, p_slip=0.08)
        updated = update(original, is_correct=True)
        assert updated.p_learn == original.p_learn
        assert updated.p_guess == original.p_guess
        assert updated.p_slip == original.p_slip


class TestBKTMastery:
    def test_low_mastery_not_mastered(self):
        params = BKTParams(p_mastery=0.3)
        assert not is_mastered(params)

    def test_high_mastery_is_mastered(self):
        params = BKTParams(p_mastery=0.90)
        assert is_mastered(params)

    def test_exactly_at_threshold_is_mastered(self):
        params = BKTParams(p_mastery=0.85)
        assert is_mastered(params, threshold=0.85)

    def test_custom_threshold(self):
        params = BKTParams(p_mastery=0.75)
        assert is_mastered(params, threshold=0.70)
        assert not is_mastered(params, threshold=0.80)


class TestPCorrectNext:
    def test_high_mastery_high_p_correct(self):
        params = BKTParams(p_mastery=0.95, p_slip=0.05, p_guess=0.20)
        p = p_correct_next(params)
        assert p > 0.75

    def test_low_mastery_p_correct_near_guess(self):
        params = BKTParams(p_mastery=0.0, p_slip=0.1, p_guess=0.25)
        p = p_correct_next(params)
        assert p == pytest.approx(0.25, abs=0.01)

    def test_p_correct_between_0_and_1(self):
        for mastery in [0.0, 0.2, 0.5, 0.8, 1.0]:
            params = BKTParams(p_mastery=mastery)
            p = p_correct_next(params)
            assert 0.0 <= p <= 1.0


class TestAccuracy:
    def test_accuracy_zero_attempts(self):
        params = BKTParams()
        assert params.accuracy_pct == 0.0

    def test_accuracy_all_correct(self):
        params = BKTParams(attempts=10, correct=10)
        assert params.accuracy_pct == 1.0

    def test_accuracy_half_correct(self):
        params = BKTParams(attempts=10, correct=5)
        assert params.accuracy_pct == pytest.approx(0.5)
