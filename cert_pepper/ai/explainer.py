"""Explanation retrieval and pre-generation logic.

Pre-generation strategy:
1. Check DB cache first (ai_explanations table)
2. If not cached, generate via Anthropic API and store
3. Use domain-specific system prompt (cached via Anthropic prompt caching)
"""

from __future__ import annotations

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from cert_pepper.ai.client import generate_explanation, make_prompt_hash
from cert_pepper.ai.prompts import get_explainer_system
from cert_pepper.config import get_settings
from cert_pepper.models.content import Question


async def get_explanation(
    session: AsyncSession,
    question: Question,
    selected_answer: str,
    explanation_type: str = "full",
) -> str:
    """
    Get explanation for a question attempt.

    First checks DB cache; generates and stores if not found.
    Uses the markdown explanation for correct answers (no API cost).
    """
    settings = get_settings()

    # For correct answers, use the stored markdown explanation
    if selected_answer.upper() == question.correct_answer and question.explanation:
        return question.explanation

    # Check DB cache
    cached = await _get_cached(session, question.id, explanation_type, selected_answer)
    if cached:
        return cached

    # Generate via API
    system = get_explainer_system(question.domain_number)
    user = _build_user_message(question, selected_answer)
    model = settings.sonnet_model

    content, tokens, cache_hit = generate_explanation(
        system_prompt=system,
        user_message=user,
        model=model,
        use_cache=True,
    )

    # Store in cache
    prompt_hash = make_prompt_hash(system, user)
    await _store_explanation(
        session,
        question_id=question.id,
        explanation_type=explanation_type,
        selected_answer=selected_answer,
        model=model,
        prompt_hash=prompt_hash,
        content=content,
        tokens=tokens,
        cached=cache_hit,
    )

    return content


async def pregenerate_all(
    session: AsyncSession,
    questions: list[Question],
    progress_callback: None = None,
) -> dict[str, int]:
    """
    Pre-generate explanations for all questions.
    Generates explanations for each wrong answer option.
    """
    generated = 0
    skipped = 0
    errors = 0

    for q in questions:
        # Generate for each wrong answer
        wrong_answers = [a for a in ["A", "B", "C", "D"] if a != q.correct_answer]

        for wrong in wrong_answers:
            existing = await _get_cached(session, q.id, "full", wrong)
            if existing:
                skipped += 1
                continue

            try:
                system = get_explainer_system(q.domain_number)
                user = _build_user_message(q, wrong)
                settings = get_settings()
                content, tokens, cache_hit = generate_explanation(
                    system_prompt=system,
                    user_message=user,
                    model=settings.sonnet_model,
                    use_cache=True,
                )
                await _store_explanation(
                    session,
                    question_id=q.id,
                    explanation_type="full",
                    selected_answer=wrong,
                    model=settings.sonnet_model,
                    prompt_hash=make_prompt_hash(system, user),
                    content=content,
                    tokens=tokens,
                    cached=cache_hit,
                )
                generated += 1
            except Exception:
                errors += 1

    return {"generated": generated, "skipped": skipped, "errors": errors}


def _build_user_message(question: Question, selected_answer: str) -> str:
    """Build the user message for explanation generation."""
    options_text = "\n".join(
        f"{letter}) {text}"
        for letter, text in question.options_dict().items()
    )
    return (
        f"Question: {question.stem}\n\n"
        f"{options_text}\n\n"
        f"The student selected: {selected_answer}) {question.get_option(selected_answer)}\n"
        f"The correct answer is: {question.correct_answer}) "
        f"{question.get_option(question.correct_answer)}\n\n"
        f"Explain why the student's answer is wrong and why the correct answer is right."
    )


async def _get_cached(
    session: AsyncSession,
    question_id: int,
    explanation_type: str,
    selected_answer: str | None,
) -> str | None:
    """Retrieve cached explanation from DB."""
    result = await session.execute(
        text("""
            SELECT content FROM ai_explanations
            WHERE content_type = 'question'
            AND content_id = :qid
            AND explanation_type = :etype
            AND (selected_answer = :ans OR (selected_answer IS NULL AND :ans IS NULL))
        """),
        {
            "qid": question_id,
            "etype": explanation_type,
            "ans": selected_answer,
        },
    )
    row = result.fetchone()
    return row[0] if row else None


async def _store_explanation(
    session: AsyncSession,
    question_id: int,
    explanation_type: str,
    selected_answer: str | None,
    model: str,
    prompt_hash: str,
    content: str,
    tokens: int,
    cached: bool,
) -> None:
    """Store explanation in DB cache."""
    await session.execute(
        text("""
            INSERT OR REPLACE INTO ai_explanations
                (content_type, content_id, explanation_type, selected_answer,
                 model_used, prompt_hash, content, tokens_used, cached)
            VALUES
                ('question', :qid, :etype, :ans, :model, :hash, :content, :tokens, :cached)
        """),
        {
            "qid": question_id,
            "etype": explanation_type,
            "ans": selected_answer,
            "model": model,
            "hash": prompt_hash,
            "content": content,
            "tokens": tokens,
            "cached": 1 if cached else 0,
        },
    )
