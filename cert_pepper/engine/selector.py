"""Adaptive question selection.

Priority order:
1. FSRS cards that are overdue (state=review, past due_date)
2. FSRS learning/relearning cards that are due
3. Weak domain questions (low BKT mastery, proportional to domain weight)
4. Unseen questions (new cards), weighted by domain weight × (1 - mastery)
"""

from __future__ import annotations

import random
from datetime import datetime
from typing import Any

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


async def get_domain_accuracy(
    session: AsyncSession, user_id: int, cert_id: int
) -> dict[int, float]:
    """Return {domain_number: accuracy} from all attempts. Missing domains default to 0.0."""
    result = await session.execute(
        text("""
            SELECT d.number,
                   AVG(CASE WHEN qa.is_correct THEN 1.0 ELSE 0.0 END) AS accuracy
            FROM question_attempts qa
            JOIN questions q ON q.id = qa.question_id
            JOIN domains d ON d.id = q.domain_id
            WHERE qa.user_id = :user_id
            AND d.certification_id = :cert_id
            GROUP BY d.number
        """),
        {"user_id": user_id, "cert_id": cert_id},
    )
    return {row[0]: float(row[1]) for row in result.fetchall()}


async def get_domain_weights(session: AsyncSession, cert_id: int) -> dict[int, float]:
    """Return {domain_number: weight_fraction} from DB for a given certification."""
    result = await session.execute(
        text("SELECT number, weight_pct FROM domains WHERE certification_id = :cert_id"),
        {"cert_id": cert_id},
    )
    return {row[0]: row[1] / 100.0 for row in result.fetchall()}


async def select_question(
    session: AsyncSession,
    user_id: int,
    domain_filter: int | None = None,
    cert_id: int | None = None,
    now: datetime | None = None,
) -> int | None:
    """
    Return a question_id to study next, or None if no questions available.

    Selection strategy:
    1. Due FSRS review cards (overdue first)
    2. Due FSRS learning cards
    3. Unseen questions weighted by domain priority
    4. Any unseen question (least recently attempted)
    """
    if now is None:
        now = datetime.utcnow()

    if cert_id is None:
        from cert_pepper.db.exams import resolve_cert_id
        cert_id = await resolve_cert_id(session)

    params: dict[str, Any] = {
        "user_id": user_id,
        "now": now,
        "cert_id": cert_id,
        "domain_filter": domain_filter,
    }

    # 1. Overdue review cards
    result = await session.execute(
        text("""
            SELECT q.id
            FROM questions q
            JOIN domains d ON d.id = q.domain_id
            JOIN fsrs_cards fc ON fc.content_type = 'question'
                AND fc.content_id = q.id AND fc.user_id = :user_id
            WHERE fc.state = 'review'
            AND fc.due_date <= :now
            AND d.certification_id = :cert_id
            AND (:domain_filter IS NULL OR d.number = :domain_filter)
            ORDER BY fc.due_date ASC
            LIMIT 1
        """),
        params,
    )
    row = result.fetchone()
    if row:
        return int(row[0])

    # 2. Due learning/relearning cards
    result = await session.execute(
        text("""
            SELECT q.id
            FROM questions q
            JOIN domains d ON d.id = q.domain_id
            JOIN fsrs_cards fc ON fc.content_type = 'question'
                AND fc.content_id = q.id AND fc.user_id = :user_id
            WHERE fc.state IN ('learning', 'relearning')
            AND fc.due_date <= :now
            AND d.certification_id = :cert_id
            AND (:domain_filter IS NULL OR d.number = :domain_filter)
            ORDER BY fc.due_date ASC
            LIMIT 1
        """),
        params,
    )
    row = result.fetchone()
    if row:
        return int(row[0])

    # 3. Unseen questions — one random candidate per domain, then weighted selection
    result = await session.execute(
        text("""
            WITH ranked AS (
                SELECT q.id, d.number AS domain_num,
                       ROW_NUMBER() OVER (PARTITION BY d.number ORDER BY RANDOM()) AS rn
                FROM questions q
                JOIN domains d ON d.id = q.domain_id
                WHERE NOT EXISTS (
                    SELECT 1 FROM fsrs_cards fc
                    WHERE fc.content_type = 'question'
                    AND fc.content_id = q.id
                    AND fc.user_id = :user_id
                )
                AND d.certification_id = :cert_id
                AND (:domain_filter IS NULL OR d.number = :domain_filter)
            )
            SELECT id, domain_num FROM ranked WHERE rn = 1
        """),
        params,
    )
    rows = result.fetchall()
    if rows:
        domain_weights = await get_domain_weights(session, cert_id)
        domain_accuracy = await get_domain_accuracy(session, user_id, cert_id)
        MIN_FLOOR = 0.1
        weights = [
            domain_weights.get(row[1], 0.2) * max(MIN_FLOOR, 1.0 - domain_accuracy.get(row[1], 0.0))
            for row in rows
        ]
        total = sum(weights)
        if total > 0:
            probs = [w / total for w in weights]
            chosen = random.choices([row[0] for row in rows], weights=probs, k=1)[0]
            return int(chosen)
        return int(rows[0][0])

    # 4. Anything — least recently attempted
    result = await session.execute(
        text("""
            SELECT q.id
            FROM questions q
            JOIN domains d ON d.id = q.domain_id
            LEFT JOIN question_attempts qa ON qa.question_id = q.id AND qa.user_id = :user_id
            WHERE d.certification_id = :cert_id
            AND (:domain_filter IS NULL OR d.number = :domain_filter)
            GROUP BY q.id
            ORDER BY MAX(qa.created_at) ASC NULLS FIRST
            LIMIT 1
        """),
        params,
    )
    row = result.fetchone()
    return int(row[0]) if row else None


async def select_exam_questions(
    session: AsyncSession,
    user_id: int,
    total: int = 90,
    cert_id: int | None = None,
) -> list[int]:
    """Select questions proportionally by domain weight for a mock exam."""
    if cert_id is None:
        from cert_pepper.db.exams import resolve_cert_id
        cert_id = await resolve_cert_id(session)

    domain_weights = await get_domain_weights(session, cert_id)
    question_ids: list[int] = []

    for domain_num, weight in domain_weights.items():
        count = round(total * weight)
        result = await session.execute(
            text("""
                SELECT q.id
                FROM questions q
                JOIN domains d ON d.id = q.domain_id
                WHERE d.number = :domain_num
                AND d.certification_id = :cert_id
                ORDER BY RANDOM()
                LIMIT :count
            """),
            {"domain_num": domain_num, "count": count, "cert_id": cert_id},
        )
        question_ids.extend(row[0] for row in result.fetchall())

    # Shuffle final list
    random.shuffle(question_ids)

    # Trim to exact total
    if len(question_ids) > total:
        question_ids = question_ids[:total]

    return question_ids
