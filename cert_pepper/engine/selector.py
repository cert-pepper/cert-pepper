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

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


DOMAIN_WEIGHTS = {1: 0.12, 2: 0.22, 3: 0.18, 4: 0.28, 5: 0.20}


async def select_question(
    session: AsyncSession,
    user_id: int,
    domain_filter: int | None = None,
    now: datetime | None = None,
) -> int | None:
    """
    Return a question_id to study next, or None if no questions available.

    Selection strategy:
    1. Due FSRS review cards (overdue first)
    2. Due FSRS learning cards
    3. Weak domain new questions
    4. Any unseen question
    """
    if now is None:
        now = datetime.utcnow()

    domain_clause = f"AND q.domain_id = (SELECT id FROM domains WHERE number = {domain_filter})" if domain_filter else ""

    # 1. Overdue review cards
    result = await session.execute(
        text(f"""
            SELECT q.id
            FROM questions q
            JOIN fsrs_cards fc ON fc.content_type = 'question' AND fc.content_id = q.id AND fc.user_id = :user_id
            WHERE fc.state = 'review'
            AND fc.due_date <= :now
            {domain_clause}
            ORDER BY fc.due_date ASC
            LIMIT 1
        """),
        {"user_id": user_id, "now": now},
    )
    row = result.fetchone()
    if row:
        return row[0]

    # 2. Due learning/relearning cards
    result = await session.execute(
        text(f"""
            SELECT q.id
            FROM questions q
            JOIN fsrs_cards fc ON fc.content_type = 'question' AND fc.content_id = q.id AND fc.user_id = :user_id
            WHERE fc.state IN ('learning', 'relearning')
            AND fc.due_date <= :now
            {domain_clause}
            ORDER BY fc.due_date ASC
            LIMIT 1
        """),
        {"user_id": user_id, "now": now},
    )
    row = result.fetchone()
    if row:
        return row[0]

    # 3. Unseen questions — weighted by domain priority
    result = await session.execute(
        text(f"""
            SELECT q.id, d.number as domain_num
            FROM questions q
            JOIN domains d ON d.id = q.domain_id
            WHERE NOT EXISTS (
                SELECT 1 FROM fsrs_cards fc
                WHERE fc.content_type = 'question'
                AND fc.content_id = q.id
                AND fc.user_id = :user_id
            )
            {domain_clause}
            ORDER BY d.weight_pct DESC, RANDOM()
            LIMIT 20
        """),
        {"user_id": user_id},
    )
    rows = result.fetchall()
    if rows:
        # Weight by domain priority
        weights = [DOMAIN_WEIGHTS.get(row[1], 0.2) for row in rows]
        total = sum(weights)
        if total > 0:
            probs = [w / total for w in weights]
            chosen = random.choices([row[0] for row in rows], weights=probs, k=1)[0]
            return chosen
        return rows[0][0]

    # 4. Anything — least recently attempted
    result = await session.execute(
        text(f"""
            SELECT q.id
            FROM questions q
            LEFT JOIN question_attempts qa ON qa.question_id = q.id AND qa.user_id = :user_id
            {("JOIN domains d ON d.id = q.domain_id " + domain_clause.replace("AND", "WHERE", 1)) if domain_clause else ""}
            GROUP BY q.id
            ORDER BY MAX(qa.created_at) ASC NULLS FIRST
            LIMIT 1
        """),
        {"user_id": user_id},
    )
    row = result.fetchone()
    return row[0] if row else None


async def select_exam_questions(
    session: AsyncSession,
    user_id: int,
    total: int = 90,
) -> list[int]:
    """Select questions proportionally by domain weight for a mock exam."""
    question_ids: list[int] = []

    for domain_num, weight in DOMAIN_WEIGHTS.items():
        count = round(total * weight)
        result = await session.execute(
            text("""
                SELECT q.id
                FROM questions q
                JOIN domains d ON d.id = q.domain_id
                WHERE d.number = :domain_num
                ORDER BY RANDOM()
                LIMIT :count
            """),
            {"domain_num": domain_num, "count": count},
        )
        question_ids.extend(row[0] for row in result.fetchall())

    # Shuffle final list
    random.shuffle(question_ids)

    # Trim or pad to exact total
    if len(question_ids) > total:
        question_ids = question_ids[:total]

    return question_ids
