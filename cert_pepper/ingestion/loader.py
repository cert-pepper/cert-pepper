"""Database loader: insert parsed content into SQLite."""

from __future__ import annotations

from pathlib import Path

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from cert_pepper.config import Settings
from cert_pepper.ingestion.questions import parse_all_questions
from cert_pepper.ingestion.flashcards import parse_flashcards
from cert_pepper.ingestion.acronyms import parse_acronyms
from cert_pepper.models.content import ParsedQuestion, ParsedFlashcard, ParsedAcronym


async def get_domain_id(session: AsyncSession, domain_number: int) -> int | None:
    """Look up domain id by number."""
    result = await session.execute(
        text("SELECT id FROM domains WHERE number = :num"),
        {"num": domain_number},
    )
    row = result.fetchone()
    return row[0] if row else None


async def ingest_questions(
    session: AsyncSession,
    questions: list[ParsedQuestion],
    dry_run: bool = False,
) -> int:
    """Insert questions into DB. Returns count inserted."""
    count = 0
    for q in questions:
        domain_id = await get_domain_id(session, q.domain_number)
        if domain_id is None:
            continue

        if not dry_run:
            await session.execute(
                text("""
                    INSERT OR REPLACE INTO questions
                        (domain_id, number, stem, option_a, option_b, option_c, option_d,
                         correct_answer, explanation, source_file)
                    VALUES
                        (:domain_id, :number, :stem, :a, :b, :c, :d,
                         :correct, :explanation, :source)
                """),
                {
                    "domain_id": domain_id,
                    "number": q.number,
                    "stem": q.stem,
                    "a": q.option_a,
                    "b": q.option_b,
                    "c": q.option_c,
                    "d": q.option_d,
                    "correct": q.correct_answer,
                    "explanation": q.explanation,
                    "source": q.source_file,
                },
            )
        count += 1
    return count


async def ingest_flashcards(
    session: AsyncSession,
    flashcards: list[ParsedFlashcard],
    dry_run: bool = False,
) -> int:
    """Insert flashcards into DB. Returns count inserted."""
    count = 0
    for fc in flashcards:
        if not dry_run:
            await session.execute(
                text("""
                    INSERT OR REPLACE INTO flashcards
                        (category, front, back, tip)
                    VALUES (:category, :front, :back, :tip)
                """),
                {
                    "category": fc.category,
                    "front": fc.front,
                    "back": fc.back,
                    "tip": fc.tip,
                },
            )
        count += 1
    return count


async def ingest_acronyms(
    session: AsyncSession,
    acronyms: list[ParsedAcronym],
    dry_run: bool = False,
) -> int:
    """Insert acronyms into DB. Returns count inserted."""
    count = 0
    for acr in acronyms:
        if not dry_run:
            await session.execute(
                text("""
                    INSERT OR REPLACE INTO acronyms (acronym, full_term, category)
                    VALUES (:acronym, :full_term, :category)
                """),
                {
                    "acronym": acr.acronym,
                    "full_term": acr.full_term,
                    "category": acr.category,
                },
            )
        count += 1
    return count


async def run_ingestion(
    session: AsyncSession,
    settings: Settings,
    dry_run: bool = False,
) -> dict[str, int]:
    """Parse all content files and insert into DB."""
    # Questions
    questions = parse_all_questions(settings.questions_dir)
    q_count = await ingest_questions(session, questions, dry_run=dry_run)

    # Flashcards
    flashcards = parse_flashcards(settings.flashcards_path)
    fc_count = await ingest_flashcards(session, flashcards, dry_run=dry_run)

    # Acronyms
    acronyms = parse_acronyms(settings.acronyms_path)
    acr_count = await ingest_acronyms(session, acronyms, dry_run=dry_run)

    return {
        "questions": q_count,
        "flashcards": fc_count,
        "acronyms": acr_count,
    }
