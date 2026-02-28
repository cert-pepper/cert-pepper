"""Database loader: insert parsed content into SQLite."""

from __future__ import annotations

from pathlib import Path

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from cert_pepper.config import Settings
from cert_pepper.ingestion.questions import parse_all_questions
from cert_pepper.ingestion.flashcards import parse_flashcards
from cert_pepper.ingestion.acronyms import parse_acronyms
from cert_pepper.models.content import ExamConfig, ParsedQuestion, ParsedFlashcard, ParsedAcronym


async def ingest_exam_config(session: AsyncSession, exam: ExamConfig) -> int:
    """Upsert certification and domains from ExamConfig. Returns cert_id."""
    # Upsert certification (INSERT OR IGNORE — code is unique)
    await session.execute(
        text(
            "INSERT OR IGNORE INTO certifications (code, name, vendor) "
            "VALUES (:code, :name, :vendor)"
        ),
        {"code": exam.code, "name": exam.name, "vendor": exam.vendor},
    )
    result = await session.execute(
        text("SELECT id FROM certifications WHERE code = :code"),
        {"code": exam.code},
    )
    cert_id: int = result.scalar()  # type: ignore[assignment]

    # Upsert each domain (update name and weight if code matches)
    for domain in exam.domains:
        await session.execute(
            text("""
                INSERT INTO domains (certification_id, number, name, weight_pct)
                VALUES (:cert_id, :number, :name, :weight)
                ON CONFLICT(certification_id, number) DO UPDATE SET
                    name=excluded.name,
                    weight_pct=excluded.weight_pct
            """),
            {
                "cert_id": cert_id,
                "number": domain.number,
                "name": domain.name,
                "weight": domain.weight_pct,
            },
        )

    return cert_id


async def get_domain_id(
    session: AsyncSession,
    domain_number: int,
    cert_id: int | None = None,
) -> int | None:
    """Look up domain id by number, optionally scoped to a certification."""
    if cert_id is not None:
        result = await session.execute(
            text("SELECT id FROM domains WHERE number = :num AND certification_id = :cert_id"),
            {"num": domain_number, "cert_id": cert_id},
        )
    else:
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
    cert_id: int | None = None,
) -> int:
    """Insert questions into DB. Returns count inserted."""
    count = 0
    for q in questions:
        domain_id = await get_domain_id(session, q.domain_number, cert_id=cert_id)
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
    cert_id: int | None = None,
) -> int:
    """Insert flashcards into DB. Returns count inserted."""
    count = 0
    for fc in flashcards:
        if not dry_run:
            await session.execute(
                text("""
                    INSERT OR REPLACE INTO flashcards
                        (category, front, back, tip, certification_id)
                    VALUES (:category, :front, :back, :tip, :cert_id)
                """),
                {
                    "category": fc.category,
                    "front": fc.front,
                    "back": fc.back,
                    "tip": fc.tip,
                    "cert_id": cert_id,
                },
            )
        count += 1
    return count


async def ingest_acronyms(
    session: AsyncSession,
    acronyms: list[ParsedAcronym],
    dry_run: bool = False,
    cert_id: int | None = None,
) -> int:
    """Insert acronyms into DB. Returns count inserted."""
    count = 0
    for acr in acronyms:
        if not dry_run:
            await session.execute(
                text("""
                    INSERT OR REPLACE INTO acronyms (acronym, full_term, category, certification_id)
                    VALUES (:acronym, :full_term, :category, :cert_id)
                """),
                {
                    "acronym": acr.acronym,
                    "full_term": acr.full_term,
                    "category": acr.category,
                    "cert_id": cert_id,
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
    # Parse exam.yaml to get certification + domain config
    exam_yaml_path = settings.content_root / "exam.yaml"
    cert_id: int | None = None

    if exam_yaml_path.exists():
        from cert_pepper.ingestion.exam_yaml import parse_exam_yaml
        exam = parse_exam_yaml(exam_yaml_path)
        if not dry_run:
            cert_id = await ingest_exam_config(session, exam)
        else:
            # In dry_run, resolve existing cert_id without writing
            from cert_pepper.db.exams import resolve_cert_id
            try:
                cert_id = await resolve_cert_id(session, exam.code)
            except ValueError:
                cert_id = None

    # Questions
    questions = parse_all_questions(settings.questions_dir)
    q_count = await ingest_questions(session, questions, dry_run=dry_run, cert_id=cert_id)

    # Flashcards
    flashcards = parse_flashcards(settings.flashcards_path)
    fc_count = await ingest_flashcards(session, flashcards, dry_run=dry_run, cert_id=cert_id)

    # Acronyms
    acronyms = parse_acronyms(settings.acronyms_path)
    acr_count = await ingest_acronyms(session, acronyms, dry_run=dry_run, cert_id=cert_id)

    return {
        "questions": q_count,
        "flashcards": fc_count,
        "acronyms": acr_count,
    }
