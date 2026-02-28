"""Predicted score calculator.

Security+ scores: 100-900 scale, passing = 750.
Predicted score = Σ(domain_accuracy × domain_weight) × 900
Pass probability uses logistic function centered on 750.
"""

from __future__ import annotations

import math

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from cert_pepper.models.analytics import (
    PredictedScore,
    WeakArea,
    StudyRecommendation,
)

PASSING_SCORE = 750
MAX_SCORE = 900
WEAK_AREA_THRESHOLD = 0.70


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

    accuracies = await get_domain_accuracies(session, user_id, cert_id=cert_id)
    d_acc = {num: accuracies.get(num, (0.0, 0))[0] for num in db_weights}

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
