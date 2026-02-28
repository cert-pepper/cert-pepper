"""FSRS-4.5 (Free Spaced Repetition Scheduler) implementation.

References:
  - https://github.com/open-spaced-repetition/fsrs4anki/wiki/The-Algorithm
  - FSRS-4.5 paper: https://arxiv.org/abs/2402.05134

Key concepts:
  - S (Stability): how long until 90% retention; grows with good reviews
  - D (Difficulty): inherent item difficulty on a 1–10 scale (higher = harder)
  - R (Retrievability): P(recall) = (1 + FACTOR*t/S)^DECAY — drops over time
  - States: new → learning → review → relearning
  - Ratings: 1=Again, 2=Hard, 3=Good, 4=Easy
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from datetime import datetime, timedelta

# FSRS-4.5 default parameters (w0..w18)
# These are the optimized weights from the paper
W = [
    0.4072, 1.1829, 3.1262, 15.4722,  # w0-w3: initial stability for ratings 1-4
    7.2102, 0.5316, 1.0651, 0.0589,   # w4-w7
    1.5330, 0.1544, 0.9597, 2.0246,   # w8-w11
    0.0070, 0.4050, 2.9898, 0.1100,   # w12-w15
    2.9898, 0.3400, 1.3001,           # w16-w18
]

DECAY = -0.5
FACTOR = 0.9 ** (1 / DECAY) - 1  # ≈ 19/81 ≈ 0.2346

# Learning steps in minutes
LEARNING_STEPS = [1, 10]
# Relearning steps in minutes
RELEARNING_STEPS = [10]

REQUEST_RETENTION = 0.9  # target retention rate


@dataclass
class FSRSCard:
    """Mutable FSRS state for a single card (not the DB model).

    Note: difficulty is on a 1-10 scale (higher = harder).
    """
    stability: float = 1.0
    difficulty: float = 5.0   # midpoint of 1-10 scale
    retrievability: float = 1.0
    due_date: datetime = field(default_factory=datetime.utcnow)
    last_review: datetime | None = None
    state: str = "new"   # new | learning | review | relearning
    step: int = 0        # index into learning/relearning steps
    reps: int = 0
    lapses: int = 0


def retrievability(stability: float, elapsed_days: float) -> float:
    """R(t) = (1 + FACTOR * t / S) ^ DECAY."""
    if elapsed_days <= 0:
        return 1.0
    return float((1 + FACTOR * elapsed_days / stability) ** DECAY)


def initial_stability(rating: int) -> float:
    """S0 based on first rating (w0..w3)."""
    return W[rating - 1]


def initial_difficulty(rating: int) -> float:
    """D0 based on first rating. Difficulty is on a 1-10 scale (higher = harder)."""
    # D0 = w4 - exp(w5 * (rating - 1)) + 1, clamped to [1.0, 10.0]
    d = W[4] - math.exp(W[5] * (rating - 1)) + 1
    return max(1.0, min(10.0, d))


def next_difficulty(d: float, rating: int) -> float:
    """Update difficulty after a review. D is on 1-10 scale."""
    # delta_d = -w6 * (rating - 3)
    delta_d = -W[6] * (rating - 3)
    # mean reversion: w7 * D0(4) pulls toward the mean
    d_new = d + delta_d + W[7] * (initial_difficulty(4) - d)
    return max(1.0, min(10.0, d_new))


def short_term_stability(s: float, rating: int) -> float:
    """Stability after a same-day (short-term) review."""
    # S' = S * exp(w17 * (rating - 3 + w18))
    return s * math.exp(W[17] * (rating - 3 + W[18]))


def stability_after_recall(d: float, s: float, r: float, rating: int) -> float:
    """Stability after a successful recall (rating ≥ 2)."""
    # S'_r = S * (exp(w8) * (11 - D) * S^-w9 * (exp(w10*(1-R)) - 1) * hard_penalty * easy_bonus + 1)
    hard_penalty = W[15] if rating == 2 else 1.0
    easy_bonus = W[16] if rating == 4 else 1.0
    s_new = s * (
        math.exp(W[8])
        * (11 - d)
        * (s ** -W[9])
        * (math.exp(W[10] * (1 - r)) - 1)
        * hard_penalty
        * easy_bonus
        + 1
    )
    return float(max(s, s_new))  # stability should only grow on recall


def stability_after_forget(d: float, s: float, r: float) -> float:
    """Stability after a lapse (rating = 1)."""
    # S'_f = w11 * D^-w12 * ((S+1)^w13 - 1) * exp(w14 * (1-R))
    s_new = (
        W[11]
        * (d ** -W[12])
        * ((s + 1) ** W[13] - 1)
        * math.exp(W[14] * (1 - r))
    )
    return float(max(0.1, min(s, s_new)))  # lapse reduces stability


def next_interval(stability: float, target_retention: float = REQUEST_RETENTION) -> float:
    """Calculate next review interval in days."""
    # I = S / FACTOR * (target_retention^(1/DECAY) - 1)
    interval = stability / FACTOR * (target_retention ** (1 / DECAY) - 1)
    return float(max(1.0, interval))


def schedule(card: FSRSCard, rating: int, now: datetime | None = None) -> FSRSCard:
    """
    Update card state after a review and return updated card.

    Args:
        card: Current FSRS card state
        rating: 1=Again, 2=Hard, 3=Good, 4=Easy
        now: Review timestamp (defaults to utcnow)

    Returns:
        Updated FSRSCard with new stability, difficulty, due_date, state
    """
    if now is None:
        now = datetime.utcnow()

    elapsed_days = 0.0
    if card.last_review is not None:
        elapsed_days = (now - card.last_review).total_seconds() / 86400

    r = retrievability(card.stability, elapsed_days) if card.state == "review" else 1.0

    # --- State machine ---
    new_card = FSRSCard(
        stability=card.stability,
        difficulty=card.difficulty,
        retrievability=r,
        last_review=now,
        reps=card.reps + 1,
        lapses=card.lapses,
    )

    if card.state == "new":
        # First encounter
        new_card.difficulty = initial_difficulty(rating)
        new_card.stability = initial_stability(rating)

        if rating == 1:
            # Again: stay in learning, step 0
            new_card.state = "learning"
            new_card.step = 0
            new_card.due_date = now + timedelta(minutes=LEARNING_STEPS[0])
        elif rating == 2:
            # Hard: learning step 0
            new_card.state = "learning"
            new_card.step = 0
            new_card.due_date = now + timedelta(minutes=LEARNING_STEPS[0])
        elif rating == 3:
            # Good: advance to step 1 if it exists
            if len(LEARNING_STEPS) > 1:
                new_card.state = "learning"
                new_card.step = 1
                new_card.due_date = now + timedelta(minutes=LEARNING_STEPS[1])
            else:
                new_card.state = "review"
                new_card.due_date = now + timedelta(days=max(1, next_interval(new_card.stability)))
        else:
            # Easy: graduate immediately
            new_card.state = "review"
            new_card.stability = short_term_stability(new_card.stability, rating)
            interval = next_interval(new_card.stability)
            new_card.due_date = now + timedelta(days=interval)

    elif card.state == "learning":
        new_card.difficulty = next_difficulty(card.difficulty, rating)

        if rating == 1:
            # Again: back to step 0
            new_card.state = "learning"
            new_card.step = 0
            new_card.stability = short_term_stability(card.stability, rating)
            new_card.due_date = now + timedelta(minutes=LEARNING_STEPS[0])
        elif rating == 2:
            # Hard: stay at current step
            new_card.state = "learning"
            new_card.step = card.step
            new_card.stability = short_term_stability(card.stability, rating)
            new_card.due_date = now + timedelta(minutes=LEARNING_STEPS[card.step])
        elif rating == 3:
            # Good: advance step or graduate
            next_step = card.step + 1
            if next_step < len(LEARNING_STEPS):
                new_card.state = "learning"
                new_card.step = next_step
                new_card.stability = short_term_stability(card.stability, rating)
                new_card.due_date = now + timedelta(minutes=LEARNING_STEPS[next_step])
            else:
                new_card.state = "review"
                new_card.stability = short_term_stability(card.stability, rating)
                interval = next_interval(new_card.stability)
                new_card.due_date = now + timedelta(days=interval)
        else:
            # Easy: graduate immediately with bonus
            new_card.state = "review"
            new_card.stability = short_term_stability(card.stability, rating)
            interval = next_interval(new_card.stability) * W[16]
            new_card.due_date = now + timedelta(days=max(1, interval))

    elif card.state == "review":
        new_card.difficulty = next_difficulty(card.difficulty, rating)

        if rating == 1:
            # Lapse: move to relearning
            new_card.lapses = card.lapses + 1
            new_card.state = "relearning"
            new_card.step = 0
            new_card.stability = stability_after_forget(card.difficulty, card.stability, r)
            new_card.due_date = now + timedelta(minutes=RELEARNING_STEPS[0])
        else:
            # Recall: update stability and schedule next review
            new_card.stability = stability_after_recall(card.difficulty, card.stability, r, rating)
            interval = next_interval(new_card.stability)
            new_card.state = "review"
            new_card.due_date = now + timedelta(days=interval)

        new_card.retrievability = retrievability(new_card.stability, 0)

    elif card.state == "relearning":
        new_card.difficulty = next_difficulty(card.difficulty, rating)

        if rating == 1:
            # Still failing: back to step 0
            new_card.state = "relearning"
            new_card.step = 0
            new_card.stability = short_term_stability(card.stability, rating)
            new_card.due_date = now + timedelta(minutes=RELEARNING_STEPS[0])
        else:
            # Advance step or graduate back to review
            next_step = card.step + 1
            if next_step < len(RELEARNING_STEPS):
                new_card.state = "relearning"
                new_card.step = next_step
                new_card.stability = short_term_stability(card.stability, rating)
                new_card.due_date = now + timedelta(minutes=RELEARNING_STEPS[next_step])
            else:
                new_card.state = "review"
                new_card.stability = short_term_stability(card.stability, rating)
                interval = next_interval(new_card.stability)
                new_card.due_date = now + timedelta(days=interval)

    return new_card


def is_due(card: FSRSCard, now: datetime | None = None) -> bool:
    """Return True if the card is due for review."""
    if now is None:
        now = datetime.utcnow()
    return card.due_date <= now


def days_until_due(card: FSRSCard, now: datetime | None = None) -> float:
    """Return days until the card is due (negative if overdue)."""
    if now is None:
        now = datetime.utcnow()
    return (card.due_date - now).total_seconds() / 86400
