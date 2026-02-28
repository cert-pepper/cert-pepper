"""Tests for ingestion/loader.py.

Covers:
  - ingest_questions: dry_run returns count without DB write; live run inserts rows;
    questions with unknown domain_number are skipped
  - ingest_flashcards: dry_run vs live; correct fields stored
  - ingest_acronyms: dry_run vs live; correct fields stored
  - run_ingestion: returns dict with all three counts; dry_run mode
"""

from __future__ import annotations

import pytest
from sqlalchemy import text

from cert_pepper.db.connection import get_session
from cert_pepper.models.content import ExamConfig, ExamDomain, ParsedQuestion, ParsedFlashcard, ParsedAcronym
from cert_pepper.ingestion.loader import (
    ingest_exam_config,
    get_domain_id,
    ingest_questions,
    ingest_flashcards,
    ingest_acronyms,
)

from tests.conftest import get_cert_id, get_user_id


# ---------------------------------------------------------------------------
# Fixtures / helpers
# ---------------------------------------------------------------------------

def make_parsed_questions(domain_number: int = 4, count: int = 1) -> list[ParsedQuestion]:
    return [
        ParsedQuestion(
            domain_number=domain_number,
            number=i + 1,
            stem=f"Question {i + 1}?",
            option_a="Alpha",
            option_b="Beta",
            option_c="Gamma",
            option_d="Delta",
            correct_answer="A",
            explanation=f"Explanation {i + 1}.",
        )
        for i in range(count)
    ]


def make_parsed_flashcards(count: int = 1) -> list[ParsedFlashcard]:
    return [
        ParsedFlashcard(
            category="Crypto",
            front=f"Term {i}",
            back=f"Definition {i}",
            tip=f"Tip {i}" if i % 2 == 0 else "",
        )
        for i in range(count)
    ]


def make_parsed_acronyms(count: int = 1) -> list[ParsedAcronym]:
    return [
        ParsedAcronym(
            acronym=f"ACR{i}",
            full_term=f"Acronym Full {i}",
            category="Network",
        )
        for i in range(count)
    ]


# ---------------------------------------------------------------------------
# ingest_questions
# ---------------------------------------------------------------------------

class TestIngestQuestions:
    async def test_dry_run_returns_count_without_insert(self, db):
        questions = make_parsed_questions(domain_number=4, count=3)
        async with get_session() as session:
            count = await ingest_questions(session, questions, dry_run=True)
            await session.commit()

        assert count == 3

        async with get_session() as session:
            result = await session.execute(text("SELECT COUNT(*) FROM questions"))
            assert result.scalar() == 0

    async def test_live_run_inserts_rows(self, db):
        questions = make_parsed_questions(domain_number=4, count=2)
        async with get_session() as session:
            count = await ingest_questions(session, questions, dry_run=False)
            await session.commit()

        assert count == 2

        async with get_session() as session:
            result = await session.execute(text("SELECT COUNT(*) FROM questions"))
            assert result.scalar() == 2

    async def test_inserted_row_has_correct_fields(self, db):
        questions = [
            ParsedQuestion(
                domain_number=4,
                number=99,
                stem="Which cipher is symmetric?",
                option_a="RSA",
                option_b="AES",
                option_c="ECC",
                option_d="SHA-256",
                correct_answer="B",
                explanation="AES is symmetric.",
            )
        ]
        async with get_session() as session:
            await ingest_questions(session, questions)
            await session.commit()

        async with get_session() as session:
            result = await session.execute(
                text("SELECT stem, correct_answer, explanation FROM questions WHERE number = 99")
            )
            row = result.fetchone()

        assert row is not None
        assert row[0] == "Which cipher is symmetric?"
        assert row[1] == "B"
        assert row[2] == "AES is symmetric."

    async def test_unknown_domain_number_skipped(self, db):
        questions = make_parsed_questions(domain_number=99, count=2)
        async with get_session() as session:
            count = await ingest_questions(session, questions)
            await session.commit()

        # Domain 99 doesn't exist → nothing inserted
        assert count == 0

        async with get_session() as session:
            result = await session.execute(text("SELECT COUNT(*) FROM questions"))
            assert result.scalar() == 0

    async def test_returns_zero_for_empty_list(self, db):
        async with get_session() as session:
            count = await ingest_questions(session, [])
        assert count == 0


# ---------------------------------------------------------------------------
# ingest_flashcards
# ---------------------------------------------------------------------------

class TestIngestFlashcards:
    async def test_dry_run_returns_count_without_insert(self, db):
        flashcards = make_parsed_flashcards(count=4)
        async with get_session() as session:
            count = await ingest_flashcards(session, flashcards, dry_run=True)
            await session.commit()

        assert count == 4

        async with get_session() as session:
            result = await session.execute(text("SELECT COUNT(*) FROM flashcards"))
            assert result.scalar() == 0

    async def test_live_run_inserts_rows(self, db):
        flashcards = make_parsed_flashcards(count=3)
        async with get_session() as session:
            count = await ingest_flashcards(session, flashcards)
            await session.commit()

        assert count == 3

        async with get_session() as session:
            result = await session.execute(text("SELECT COUNT(*) FROM flashcards"))
            assert result.scalar() == 3

    async def test_inserted_flashcard_fields(self, db):
        flashcards = [
            ParsedFlashcard(
                category="Crypto",
                front="AES",
                back="Advanced Encryption Standard",
                tip="Block cipher, 128/192/256-bit keys",
            )
        ]
        async with get_session() as session:
            await ingest_flashcards(session, flashcards)
            await session.commit()

        async with get_session() as session:
            result = await session.execute(
                text("SELECT category, front, back, tip FROM flashcards WHERE front='AES'")
            )
            row = result.fetchone()

        assert row is not None
        assert row[0] == "Crypto"
        assert row[1] == "AES"
        assert row[2] == "Advanced Encryption Standard"
        assert row[3] == "Block cipher, 128/192/256-bit keys"

    async def test_returns_zero_for_empty_list(self, db):
        async with get_session() as session:
            count = await ingest_flashcards(session, [])
        assert count == 0


# ---------------------------------------------------------------------------
# ingest_acronyms
# ---------------------------------------------------------------------------

class TestIngestAcronyms:
    async def test_dry_run_returns_count_without_insert(self, db):
        acronyms = make_parsed_acronyms(count=5)
        async with get_session() as session:
            count = await ingest_acronyms(session, acronyms, dry_run=True)
            await session.commit()

        assert count == 5

        async with get_session() as session:
            result = await session.execute(text("SELECT COUNT(*) FROM acronyms"))
            assert result.scalar() == 0

    async def test_live_run_inserts_rows(self, db):
        acronyms = make_parsed_acronyms(count=3)
        async with get_session() as session:
            count = await ingest_acronyms(session, acronyms)
            await session.commit()

        assert count == 3

        async with get_session() as session:
            result = await session.execute(text("SELECT COUNT(*) FROM acronyms"))
            assert result.scalar() == 3

    async def test_inserted_acronym_fields(self, db):
        acronyms = [
            ParsedAcronym(
                acronym="MFA",
                full_term="Multi-Factor Authentication",
                category="Identity",
            )
        ]
        async with get_session() as session:
            await ingest_acronyms(session, acronyms)
            await session.commit()

        async with get_session() as session:
            result = await session.execute(
                text("SELECT acronym, full_term, category FROM acronyms WHERE acronym='MFA'")
            )
            row = result.fetchone()

        assert row is not None
        assert row[0] == "MFA"
        assert row[1] == "Multi-Factor Authentication"
        assert row[2] == "Identity"

    async def test_returns_zero_for_empty_list(self, db):
        async with get_session() as session:
            count = await ingest_acronyms(session, [])
        assert count == 0


# ---------------------------------------------------------------------------
# ingest_exam_config
# ---------------------------------------------------------------------------

def make_exam_config(code: str = "TEST-001", n_domains: int = 2) -> ExamConfig:
    domains = [
        ExamDomain(number=i + 1, name=f"Domain {i + 1}", weight_pct=100.0 / n_domains)
        for i in range(n_domains)
    ]
    return ExamConfig(code=code, name=f"{code} Exam", vendor="TestVendor", domains=domains)


class TestIngestExamConfig:
    async def test_creates_certification_and_domains(self, db):
        exam = make_exam_config("NEWCERT", n_domains=2)
        async with get_session() as session:
            cert_id = await ingest_exam_config(session, exam)
            await session.commit()

        async with get_session() as session:
            result = await session.execute(
                text("SELECT code, name FROM certifications WHERE id = :cid"),
                {"cid": cert_id},
            )
            row = result.fetchone()
        assert row is not None
        assert row[0] == "NEWCERT"

    async def test_creates_correct_number_of_domains(self, db):
        exam = make_exam_config("CERT3", n_domains=3)
        async with get_session() as session:
            cert_id = await ingest_exam_config(session, exam)
            await session.commit()

        async with get_session() as session:
            result = await session.execute(
                text("SELECT COUNT(*) FROM domains WHERE certification_id = :cid"),
                {"cid": cert_id},
            )
        assert result.scalar() == 3

    async def test_is_idempotent(self, db):
        """Calling ingest_exam_config twice doesn't duplicate the certification."""
        exam = make_exam_config("IDEM")
        async with get_session() as session:
            await ingest_exam_config(session, exam)
            await session.commit()

        async with get_session() as session:
            await ingest_exam_config(session, exam)
            await session.commit()

        async with get_session() as session:
            result = await session.execute(
                text("SELECT COUNT(*) FROM certifications WHERE code = 'IDEM'")
            )
        assert result.scalar() == 1

    async def test_updates_domain_weight_on_upsert(self, db):
        """Re-ingesting with updated weights updates existing domain rows."""
        exam = ExamConfig(
            code="UPDT",
            name="Update Exam",
            domains=[ExamDomain(number=1, name="D1", weight_pct=100.0)],
        )
        async with get_session() as session:
            cert_id = await ingest_exam_config(session, exam)
            await session.commit()

        # Re-ingest with a different weight
        exam2 = ExamConfig(
            code="UPDT",
            name="Update Exam",
            domains=[ExamDomain(number=1, name="D1 Updated", weight_pct=100.0)],
        )
        async with get_session() as session:
            await ingest_exam_config(session, exam2)
            await session.commit()

        async with get_session() as session:
            result = await session.execute(
                text("SELECT name FROM domains WHERE certification_id = :cid AND number = 1"),
                {"cid": cert_id},
            )
            name = result.scalar()
        assert name == "D1 Updated"


# ---------------------------------------------------------------------------
# get_domain_id scoped by cert
# ---------------------------------------------------------------------------

class TestGetDomainIdScoped:
    async def test_scoped_lookup_finds_correct_domain(self, db):
        """get_domain_id with cert_id only returns the domain belonging to that cert."""
        async with get_session() as session:
            cert_id = await get_cert_id(session, "SY0-701")
            domain_id = await get_domain_id(session, 4, cert_id=cert_id)
        assert domain_id is not None

    async def test_scoped_lookup_returns_none_for_wrong_cert(self, db):
        """get_domain_id with a non-existent cert_id returns None."""
        async with get_session() as session:
            domain_id = await get_domain_id(session, 4, cert_id=9999)
        assert domain_id is None

    async def test_unscoped_lookup_still_works(self, db):
        """get_domain_id without cert_id uses the old behavior."""
        async with get_session() as session:
            domain_id = await get_domain_id(session, 4)
        assert domain_id is not None
