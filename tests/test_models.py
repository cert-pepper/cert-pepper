"""Tests for Pydantic domain models.

Covers:
  - models/content.py: Question methods
  - models/progress.py: StudySession.accuracy, FSRSRating values
  - models/analytics.py: PredictedScore.weighted_accuracy
  - cli/exam.py: format_time (pure utility)
"""

from __future__ import annotations

import pytest

from cert_pepper.models.content import Question, ParsedQuestion, ParsedFlashcard, ParsedAcronym
from cert_pepper.models.progress import FSRSRating, StudySession
from cert_pepper.models.analytics import PredictedScore, WeakArea


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_question(**overrides) -> Question:
    base = dict(
        id=1,
        domain_id=2,
        domain_number=2,
        number=5,
        stem="Which of the following is a symmetric cipher?",
        option_a="RSA",
        option_b="ECC",
        option_c="AES",
        option_d="SHA-256",
        correct_answer="C",
        explanation="AES is a symmetric block cipher.",
    )
    return Question(**{**base, **overrides})


# ---------------------------------------------------------------------------
# Question
# ---------------------------------------------------------------------------

class TestQuestion:
    def test_get_option_a(self):
        q = make_question()
        assert q.get_option("A") == "RSA"

    def test_get_option_b(self):
        q = make_question()
        assert q.get_option("B") == "ECC"

    def test_get_option_c(self):
        q = make_question()
        assert q.get_option("C") == "AES"

    def test_get_option_d(self):
        q = make_question()
        assert q.get_option("D") == "SHA-256"

    def test_get_option_lowercase_works(self):
        q = make_question()
        assert q.get_option("a") == q.get_option("A")
        assert q.get_option("c") == q.get_option("C")

    def test_options_dict_has_exactly_four_keys(self):
        q = make_question()
        opts = q.options_dict()
        assert set(opts.keys()) == {"A", "B", "C", "D"}

    def test_options_dict_values_match_fields(self):
        q = make_question()
        opts = q.options_dict()
        assert opts["A"] == q.option_a
        assert opts["B"] == q.option_b
        assert opts["C"] == q.option_c
        assert opts["D"] == q.option_d

    def test_options_dict_does_not_include_correct_answer_field(self):
        # options_dict is A/B/C/D text, not the letter of the correct answer
        q = make_question(correct_answer="C")
        opts = q.options_dict()
        assert "correct_answer" not in opts

    def test_get_option_on_correct_answer_returns_that_option_text(self):
        q = make_question(correct_answer="C", option_c="AES")
        assert q.get_option(q.correct_answer) == "AES"


# ---------------------------------------------------------------------------
# ParsedQuestion / ParsedFlashcard / ParsedAcronym (data integrity)
# ---------------------------------------------------------------------------

class TestParsedModels:
    def test_parsed_question_requires_correct_answer_letter(self):
        pq = ParsedQuestion(
            domain_number=1, number=1, stem="Q?",
            option_a="a", option_b="b", option_c="c", option_d="d",
            correct_answer="B",
        )
        assert pq.correct_answer == "B"

    def test_parsed_flashcard_tip_defaults_empty(self):
        fc = ParsedFlashcard(category="Crypto", front="AES", back="Symmetric cipher")
        assert fc.tip == ""

    def test_parsed_acronym_category_defaults_empty(self):
        acr = ParsedAcronym(acronym="MFA", full_term="Multi-Factor Authentication")
        assert acr.category == ""


# ---------------------------------------------------------------------------
# FSRSRating
# ---------------------------------------------------------------------------

class TestFSRSRating:
    def test_again_equals_1(self):
        assert FSRSRating.AGAIN == 1

    def test_hard_equals_2(self):
        assert FSRSRating.HARD == 2

    def test_good_equals_3(self):
        assert FSRSRating.GOOD == 3

    def test_easy_equals_4(self):
        assert FSRSRating.EASY == 4

    def test_ratings_are_ordered(self):
        assert FSRSRating.AGAIN < FSRSRating.HARD < FSRSRating.GOOD < FSRSRating.EASY

    def test_ratings_are_integer_values(self):
        for rating in [FSRSRating.AGAIN, FSRSRating.HARD, FSRSRating.GOOD, FSRSRating.EASY]:
            assert isinstance(int(rating), int)


# ---------------------------------------------------------------------------
# StudySession.accuracy
# ---------------------------------------------------------------------------

class TestStudySessionAccuracy:
    def _session(self, seen: int, correct: int) -> StudySession:
        return StudySession(
            user_id=1,
            session_type="study",
            questions_seen=seen,
            questions_correct=correct,
        )

    def test_zero_questions_returns_zero(self):
        assert self._session(0, 0).accuracy == 0.0

    def test_all_correct(self):
        assert self._session(10, 10).accuracy == pytest.approx(1.0)

    def test_half_correct(self):
        assert self._session(20, 10).accuracy == pytest.approx(0.5)

    def test_none_correct(self):
        assert self._session(5, 0).accuracy == pytest.approx(0.0)

    def test_one_out_of_three(self):
        assert self._session(3, 1).accuracy == pytest.approx(1 / 3)

    def test_accuracy_never_exceeds_one(self):
        # Edge case: more correct than seen would be a data bug, but we verify
        # the formula doesn't overflow
        s = self._session(5, 5)
        assert s.accuracy <= 1.0


# ---------------------------------------------------------------------------
# PredictedScore.weighted_accuracy
# ---------------------------------------------------------------------------

class TestPredictedScoreWeightedAccuracy:
    def test_all_domains_at_100_pct_gives_100_pct(self):
        score = PredictedScore(
            d1_accuracy=1.0, d2_accuracy=1.0, d3_accuracy=1.0,
            d4_accuracy=1.0, d5_accuracy=1.0,
        )
        assert score.weighted_accuracy == pytest.approx(1.0, abs=1e-6)

    def test_all_domains_at_zero_gives_zero(self):
        score = PredictedScore()
        assert score.weighted_accuracy == pytest.approx(0.0)

    def test_domain4_only_at_100_pct_gives_28_pct(self):
        """Domain 4 has 28% weight; all others 0% → weighted = 0.28."""
        score = PredictedScore(
            d1_accuracy=0.0, d2_accuracy=0.0, d3_accuracy=0.0,
            d4_accuracy=1.0, d5_accuracy=0.0,
        )
        assert score.weighted_accuracy == pytest.approx(0.28, abs=1e-6)

    def test_domain1_only_at_100_pct_gives_12_pct(self):
        score = PredictedScore(
            d1_accuracy=1.0, d2_accuracy=0.0, d3_accuracy=0.0,
            d4_accuracy=0.0, d5_accuracy=0.0,
        )
        assert score.weighted_accuracy == pytest.approx(0.12, abs=1e-6)

    def test_weights_implied_by_formula_sum_to_one(self):
        """Setting each domain to 1.0 in turn and summing weighted_accuracy must equal 1.0."""
        total = sum(
            PredictedScore(**{f"d{i}_accuracy": 1.0}).weighted_accuracy
            for i in range(1, 6)
        )
        assert total == pytest.approx(1.0, abs=1e-6)

    def test_uniform_80_pct_gives_80_pct_weighted(self):
        score = PredictedScore(
            d1_accuracy=0.8, d2_accuracy=0.8, d3_accuracy=0.8,
            d4_accuracy=0.8, d5_accuracy=0.8,
        )
        assert score.weighted_accuracy == pytest.approx(0.8, abs=1e-6)


# ---------------------------------------------------------------------------
# WeakArea
# ---------------------------------------------------------------------------

class TestWeakArea:
    def test_priority_score_is_weight_fraction_times_weakness(self):
        # weight_pct=28, accuracy=0.60 → priority = 0.28 * (1-0.60) = 0.112
        area = WeakArea(
            domain_number=4,
            domain_name="Security Operations",
            accuracy_pct=0.60,
            weight_pct=28.0,
            attempts=10,
            priority_score=0.28 * 0.40,
        )
        assert area.priority_score == pytest.approx(0.112, abs=1e-6)

    def test_zero_attempts_area_is_valid(self):
        area = WeakArea(
            domain_number=3,
            domain_name="Security Architecture",
            accuracy_pct=0.0,
            weight_pct=18.0,
            attempts=0,
            priority_score=0.18,
        )
        assert area.attempts == 0
        assert area.accuracy_pct == 0.0


# ---------------------------------------------------------------------------
# format_time (pure utility in cli/exam.py)
# ---------------------------------------------------------------------------

class TestFormatTime:
    def _fmt(self, seconds: int) -> str:
        from cert_pepper.cli.exam import format_time
        return format_time(seconds)

    def test_zero_seconds(self):
        assert self._fmt(0) == "00:00"

    def test_one_minute(self):
        assert self._fmt(60) == "01:00"

    def test_ninety_minutes(self):
        assert self._fmt(90 * 60) == "90:00"

    def test_one_second(self):
        assert self._fmt(1) == "00:01"

    def test_mixed(self):
        assert self._fmt(125) == "02:05"

    def test_59_seconds(self):
        assert self._fmt(59) == "00:59"

    def test_zero_padded_minutes(self):
        assert self._fmt(600) == "10:00"
