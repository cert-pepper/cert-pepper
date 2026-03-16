"""Predicted score calculator.

Security+ scores: 100-900 scale, passing = 750.
Predicted score = Σ(domain_accuracy × domain_weight) × 900
Pass probability uses logistic function centered on 750.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from datetime import date, timedelta

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from cert_pepper.models.analytics import (
    PredictedScore,
    QuestionCounts,
    StudyRecommendation,
    WeakArea,
)


@dataclass
class ScheduleStatus:
    exam_date: date
    target_hours: int
    hours_completed: float
    hours_remaining: float
    days_remaining: int
    sessions_per_day: int
    sessions_today: int
    on_pace: bool
    pct_complete: float


@dataclass
class DayStatus:
    date: date
    sessions_target: int
    sessions_actual: int
    status: str  # "met" | "partial" | "missed" | "future" | "today"


_SESSION_MINUTES = 45  # assumed session length for scheduling math


def compute_schedule_status(
    exam_date: date,
    target_hours: int,
    hours_completed: float,
    sessions_today: int,
    start_date: date | None = None,
) -> ScheduleStatus:
    """Compute schedule adherence toward an exam date.

    Args:
        exam_date: Target exam date.
        target_hours: Total planned study hours.
        hours_completed: Hours studied so far (from study_sessions).
        sessions_today: Sessions already completed today.
        start_date: When goal tracking began (for on_pace calculation).
                    Defaults to 14 days before exam_date if None.
    """
    today = date.today()
    if start_date is None:
        start_date = exam_date - timedelta(days=14)

    days_remaining = max(0, (exam_date - today).days)
    hours_remaining = max(0.0, target_hours - hours_completed)
    pct_complete = min(1.0, hours_completed / target_hours) if target_hours > 0 else 0.0

    # sessions/day: how many 45-min sessions to finish remaining hours
    hours_per_day = hours_remaining / max(days_remaining, 1)
    raw_sessions = math.ceil(hours_per_day * 60 / _SESSION_MINUTES)
    sessions_per_day = max(1, min(3, raw_sessions))

    # on_pace: current required daily rate ≤ original planned daily rate
    total_days = max(1, (exam_date - start_date).days)
    planned_daily = target_hours / total_days
    required_daily = hours_remaining / max(days_remaining, 1)
    on_pace = required_daily <= planned_daily

    return ScheduleStatus(
        exam_date=exam_date,
        target_hours=target_hours,
        hours_completed=hours_completed,
        hours_remaining=hours_remaining,
        days_remaining=days_remaining,
        sessions_per_day=sessions_per_day,
        sessions_today=sessions_today,
        on_pace=on_pace,
        pct_complete=pct_complete,
    )


def get_day_statuses(
    daily_sessions: dict[date, int],
    exam_date: date,
    sessions_per_day: int,
    start_date: date,
) -> list[DayStatus]:
    """Return a DayStatus for every day from start_date to exam_date (inclusive).

    Args:
        daily_sessions: Map of {date: sessions_completed} from DB.
        exam_date: Target exam date (included in the output list).
        sessions_per_day: Recommended daily target.
        start_date: First day to include.
    """
    today = date.today()
    statuses: list[DayStatus] = []
    current = start_date
    while current <= exam_date:
        actual = daily_sessions.get(current, 0)
        if current > today:
            status = "future"
        elif current == today:
            status = "today"
        elif actual >= sessions_per_day:
            status = "met"
        elif actual > 0:
            status = "partial"
        else:
            status = "missed"
        statuses.append(
            DayStatus(
                date=current,
                sessions_target=sessions_per_day,
                sessions_actual=actual,
                status=status,
            )
        )
        current += timedelta(days=1)
    return statuses


def compute_streak(dates: list[date]) -> int:
    """Count consecutive study days ending today or yesterday (grace period).

    Args:
        dates: Study dates sorted descending, deduplicated.
    """
    if not dates:
        return 0
    today = date.today()
    yesterday = today - timedelta(days=1)
    if dates[0] not in (today, yesterday):
        return 0
    streak = 1
    for i in range(1, len(dates)):
        if dates[i] == dates[i - 1] - timedelta(days=1):
            streak += 1
        else:
            break
    return streak


PASSING_SCORE = 750
MAX_SCORE = 900
WEAK_AREA_THRESHOLD = 0.70

_PEPPER_SCALE: list[str] = [
    "Bell Pepper",
    "Banana Pepper",
    "Poblano",
    "Jalapeño",
    "Serrano",
    "Cayenne",
    "Thai Chili",
    "Habanero",
    "Ghost Pepper",
    "Carolina Reaper",
]


def pepper_score(pass_probability: float) -> tuple[int, str]:
    """Return (level, pepper_name) for a 1-10 pepper spice scale."""
    clamped = max(0.0, min(1.0, pass_probability))
    # 0.0-0.099 → 0, 0.10-0.199 → 1, ... 0.90-1.0 → 9
    index = min(int(clamped * 10), 9)
    return (index + 1, _PEPPER_SCALE[index])


async def get_domain_accuracies(
    session: AsyncSession,
    user_id: int,
    cert_id: int | None = None,
) -> dict[int, tuple[float, int]]:
    """Return {domain_number: (accuracy, attempt_count)} from all-time attempts."""
    if cert_id is None:
        from cert_pepper.db.exams import resolve_cert_id
        cert_id = await resolve_cert_id(session)

    result = await session.execute(
        text("""
            SELECT d.number,
                   COUNT(*) as total,
                   SUM(qa.is_correct) as correct
            FROM question_attempts qa
            JOIN questions q ON q.id = qa.question_id
            JOIN domains d ON d.id = q.domain_id
            WHERE qa.user_id = :user_id
            AND d.certification_id = :cert_id
            GROUP BY d.number
        """),
        {"user_id": user_id, "cert_id": cert_id},
    )
    rows = result.fetchall()
    return {
        row[0]: (row[2] / row[1] if row[1] > 0 else 0.0, row[1])
        for row in rows
    }


async def predict_score(
    session: AsyncSession,
    user_id: int,
    cert_id: int | None = None,
) -> PredictedScore:
    """Calculate predicted exam score and pass probability."""
    if cert_id is None:
        from cert_pepper.db.exams import resolve_cert_id
        cert_id = await resolve_cert_id(session)

    # Read domain weights from DB
    result = await session.execute(
        text("SELECT number, weight_pct FROM domains WHERE certification_id = :cert_id"),
        {"cert_id": cert_id},
    )
    db_weights = {row[0]: row[1] / 100.0 for row in result.fetchall()}

    # Per-domain: seen distinct questions and total question count
    cov_result = await session.execute(
        text("""
            SELECT d.number,
                   COUNT(DISTINCT qa.question_id) AS seen,
                   COUNT(DISTINCT q.id)           AS total
            FROM domains d
            JOIN questions q ON q.domain_id = d.id
            LEFT JOIN question_attempts qa
                ON qa.question_id = q.id AND qa.user_id = :user_id
            WHERE d.certification_id = :cert_id
            GROUP BY d.number
        """),
        {"user_id": user_id, "cert_id": cert_id},
    )
    domain_coverage = {row[0]: (row[1], row[2]) for row in cov_result.fetchall()}

    raw_accuracies = await get_domain_accuracies(session, user_id, cert_id=cert_id)

    d_acc: dict[int, float] = {}
    for num in db_weights:
        seen, total = domain_coverage.get(num, (0, 0))
        raw = raw_accuracies.get(num, (0.0, 0))[0]
        if total > 0:
            d_acc[num] = (raw * seen + 0.5 * (total - seen)) / total
        else:
            d_acc[num] = 0.0

    # Overall coverage fraction
    total_seen = sum(v[0] for v in domain_coverage.values())
    total_qs = sum(v[1] for v in domain_coverage.values())
    coverage_pct = total_seen / total_qs if total_qs > 0 else 0.0

    # Weighted accuracy
    weighted = sum(d_acc.get(i, 0.0) * db_weights[i] for i in db_weights)
    predicted = round(weighted * MAX_SCORE)

    # Pass probability: logistic sigmoid centered on passing_score
    k = 50  # steepness: 50 points spans ~80% of the sigmoid
    pass_prob = 1.0 / (1.0 + math.exp(-(predicted - PASSING_SCORE) / k))

    return PredictedScore(
        domain_accuracies=d_acc,
        domain_weights=db_weights,
        predicted_score=predicted,
        pass_probability=pass_prob,
        coverage_pct=coverage_pct,
    )


async def get_weak_areas(
    session: AsyncSession,
    user_id: int,
    threshold: float = WEAK_AREA_THRESHOLD,
    cert_id: int | None = None,
) -> list[WeakArea]:
    """Return domains below threshold, sorted by priority (weight × weakness)."""
    if cert_id is None:
        from cert_pepper.db.exams import resolve_cert_id
        cert_id = await resolve_cert_id(session)

    result = await session.execute(
        text("""
            SELECT d.number, d.name, d.weight_pct,
                   COUNT(*) as total,
                   SUM(qa.is_correct) as correct
            FROM question_attempts qa
            JOIN questions q ON q.id = qa.question_id
            JOIN domains d ON d.id = q.domain_id
            WHERE qa.user_id = :user_id
            AND d.certification_id = :cert_id
            GROUP BY d.number, d.name, d.weight_pct
        """),
        {"user_id": user_id, "cert_id": cert_id},
    )
    rows = result.fetchall()

    weak = []
    for row in rows:
        domain_num, name, weight, total, correct = row
        accuracy = correct / total if total > 0 else 0.0
        if accuracy < threshold:
            priority = (weight / 100) * (1 - accuracy)
            weak.append(
                WeakArea(
                    domain_number=domain_num,
                    domain_name=name,
                    accuracy_pct=accuracy,
                    weight_pct=weight,
                    attempts=total,
                    priority_score=priority,
                )
            )

    # Also include domains with no attempts (from DB)
    attempted_domains = {row[0] for row in rows}
    result = await session.execute(
        text("SELECT number, name, weight_pct FROM domains WHERE certification_id = :cert_id"),
        {"cert_id": cert_id},
    )
    all_domains = result.fetchall()
    for drow in all_domains:
        num, name, weight = drow
        if num not in attempted_domains:
            weak.append(
                WeakArea(
                    domain_number=num,
                    domain_name=name,
                    accuracy_pct=0.0,
                    weight_pct=weight,
                    attempts=0,
                    priority_score=weight / 100,
                )
            )

    return sorted(weak, key=lambda w: w.priority_score, reverse=True)


async def get_recommendations(
    session: AsyncSession,
    user_id: int,
    days_remaining: int = 10,
    cert_id: int | None = None,
) -> list[StudyRecommendation]:
    """Generate prioritized study recommendations."""
    weak_areas = await get_weak_areas(session, user_id, cert_id=cert_id)

    recommendations = []
    total_priority = sum(w.priority_score for w in weak_areas) or 1.0

    for area in weak_areas[:5]:  # Top 5 weak areas
        # Allocate study time proportional to priority
        fraction = area.priority_score / total_priority
        minutes = max(15, round(fraction * 120))  # 2 hours/day budget

        if area.attempts == 0:
            reason = "No questions attempted yet"
            urgency = "critical" if area.weight_pct >= 20 else "high"
        elif area.accuracy_pct < 0.5:
            reason = f"Low accuracy ({area.accuracy_pct:.0%}) — needs significant work"
            urgency = "critical"
        elif area.accuracy_pct < 0.65:
            reason = f"Below passing threshold ({area.accuracy_pct:.0%})"
            urgency = "high"
        else:
            reason = f"Approaching threshold ({area.accuracy_pct:.0%}) — polish needed"
            urgency = "medium"

        recommendations.append(
            StudyRecommendation(
                domain_number=area.domain_number,
                domain_name=area.domain_name,
                reason=reason,
                urgency=urgency,
                suggested_minutes=minutes,
            )
        )

    return recommendations


async def get_question_counts(
    session: AsyncSession,
    user_id: int,
    cert_id: int | None = None,
) -> QuestionCounts:
    """Return counts of new, correctly answered, and incorrectly answered questions."""
    if cert_id is None:
        from cert_pepper.db.exams import resolve_cert_id
        cert_id = await resolve_cert_id(session)

    params = {"user_id": user_id, "cert_id": cert_id}

    total = int((await session.execute(text("""
        SELECT COUNT(*) FROM questions q
        JOIN domains d ON d.id = q.domain_id
        WHERE d.certification_id = :cert_id
    """), {"cert_id": cert_id})).scalar() or 0)

    new = int((await session.execute(text("""
        SELECT COUNT(*) FROM questions q
        JOIN domains d ON d.id = q.domain_id
        LEFT JOIN question_attempts qa
            ON qa.question_id = q.id AND qa.user_id = :user_id
        WHERE d.certification_id = :cert_id AND qa.id IS NULL
    """), params)).scalar() or 0)

    correct = int((await session.execute(text("""
        SELECT COUNT(DISTINCT qa.question_id)
        FROM question_attempts qa
        JOIN questions q ON q.id = qa.question_id
        JOIN domains d ON d.id = q.domain_id
        WHERE qa.user_id = :user_id AND d.certification_id = :cert_id
        AND qa.is_correct = 1
    """), params)).scalar() or 0)

    incorrect = int((await session.execute(text("""
        SELECT COUNT(DISTINCT qa.question_id)
        FROM question_attempts qa
        JOIN questions q ON q.id = qa.question_id
        JOIN domains d ON d.id = q.domain_id
        WHERE qa.user_id = :user_id AND d.certification_id = :cert_id
        AND qa.question_id NOT IN (
            SELECT DISTINCT question_id FROM question_attempts
            WHERE user_id = :user_id AND is_correct = 1
        )
    """), params)).scalar() or 0)

    return QuestionCounts(new=new, correct=correct, incorrect=incorrect, total=total)
