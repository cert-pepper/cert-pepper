"""Bayesian Knowledge Tracing (BKT) implementation.

BKT models per-domain/topic mastery as a hidden Markov model.

States: mastered (L) or not mastered (~L)
Parameters:
  - p_mastery (L): P(mastered) — updated each attempt
  - p_learn: P(learn per attempt | was not mastered)
  - p_guess: P(correct | not mastered) — lucky guess
  - p_slip: P(incorrect | mastered) — careless mistake

Update rule (Bayes):
  If correct:
    P(L | correct) = P(correct | L) * P(L) / P(correct)
                   = (1 - p_slip) * L / ((1 - p_slip) * L + p_guess * (1 - L))

  If incorrect:
    P(L | incorrect) = P(incorrect | L) * P(L) / P(incorrect)
                     = p_slip * L / (p_slip * L + (1 - p_guess) * (1 - L))

  Then apply learning transition:
    P(L_new) = P(L | obs) + (1 - P(L | obs)) * p_learn
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class BKTParams:
    """BKT parameters for a skill."""
    p_mastery: float = 0.1   # P(mastered) — initial prior
    p_learn: float = 0.30    # P(transition to mastered per attempt)
    p_guess: float = 0.20    # P(correct | not mastered)
    p_slip: float = 0.10     # P(incorrect | mastered)
    attempts: int = 0
    correct: int = 0

    @property
    def accuracy_pct(self) -> float:
        if self.attempts == 0:
            return 0.0
        return self.correct / self.attempts


def update(params: BKTParams, is_correct: bool) -> BKTParams:
    """
    Update BKT parameters after one observation.

    Returns a new BKTParams with updated p_mastery.
    """
    L = params.p_mastery
    p_l = params.p_learn
    p_g = params.p_guess
    p_s = params.p_slip

    # Step 1: Update posterior given observation
    if is_correct:
        p_obs = (1 - p_s) * L + p_g * (1 - L)
        L_given_obs = (1 - p_s) * L / p_obs if p_obs > 0 else L
    else:
        p_obs = p_s * L + (1 - p_g) * (1 - L)
        L_given_obs = p_s * L / p_obs if p_obs > 0 else L

    # Step 2: Apply learning transition
    L_new = L_given_obs + (1 - L_given_obs) * p_l

    # Clamp to valid probability range
    L_new = max(0.0, min(1.0, L_new))

    return BKTParams(
        p_mastery=L_new,
        p_learn=p_l,
        p_guess=p_g,
        p_slip=p_s,
        attempts=params.attempts + 1,
        correct=params.correct + (1 if is_correct else 0),
    )


def is_mastered(params: BKTParams, threshold: float = 0.85) -> bool:
    """Return True if skill is considered mastered."""
    return params.p_mastery >= threshold


def p_correct_next(params: BKTParams) -> float:
    """Predicted P(correct on next attempt)."""
    L = params.p_mastery
    return (1 - params.p_slip) * L + params.p_guess * (1 - L)
