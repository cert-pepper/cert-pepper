"""Tests for setup_exam MCP tool and parse_questions_text."""

from __future__ import annotations

import json
import textwrap
from unittest.mock import AsyncMock, MagicMock

import pytest

from cert_pepper.ingestion.questions import parse_questions_text


SAMPLE_QUESTIONS_MD = textwrap.dedent("""\
    **Q1.** What does CIA stand for?

    A) Confidentiality, Integrity, Availability
    B) Control, Integrity, Access
    C) Confidentiality, Information, Access
    D) Control, Information, Availability

    <details><summary>Answer</summary>

    **A) Confidentiality, Integrity, Availability**

    The CIA triad is the foundation of security.

    </details>

    ---

    **Q2.** Which protocol provides real-time certificate revocation status?

    A) CRL
    B) OCSP
    C) CSR
    D) CA

    <details><summary>Answer</summary>

    **B) OCSP**

    OCSP provides real-time status.

    </details>
""")


class TestParseQuestionsText:
    def test_basic_parses_correct_count(self):
        questions = parse_questions_text(SAMPLE_QUESTIONS_MD, domain_number=1)
        assert len(questions) == 2

    def test_domain_number_set_from_argument(self):
        questions = parse_questions_text(SAMPLE_QUESTIONS_MD, domain_number=3)
        assert all(q.domain_number == 3 for q in questions)

    def test_correct_question_numbers(self):
        questions = parse_questions_text(SAMPLE_QUESTIONS_MD, domain_number=1)
        assert [q.number for q in questions] == [1, 2]

    def test_stem_parsed(self):
        questions = parse_questions_text(SAMPLE_QUESTIONS_MD, domain_number=1)
        assert "CIA" in questions[0].stem

    def test_options_parsed(self):
        questions = parse_questions_text(SAMPLE_QUESTIONS_MD, domain_number=1)
        q = questions[0]
        assert q.option_a != ""
        assert q.option_b != ""
        assert q.option_c != ""
        assert q.option_d != ""

    def test_correct_answer(self):
        questions = parse_questions_text(SAMPLE_QUESTIONS_MD, domain_number=1)
        assert questions[0].correct_answer == "A"
        assert questions[1].correct_answer == "B"

    def test_explanation_parsed(self):
        questions = parse_questions_text(SAMPLE_QUESTIONS_MD, domain_number=1)
        assert "CIA triad" in questions[0].explanation

    def test_numbering_offset_batch(self):
        """Questions numbered Q31-Q32 should have number 31 and 32."""
        md = textwrap.dedent("""\
            **Q31.** First batch-2 question?

            A) Alpha
            B) Beta
            C) Gamma
            D) Delta

            <details><summary>Answer</summary>

            **C) Gamma**

            Gamma is correct.

            </details>

            ---

            **Q32.** Second batch-2 question?

            A) One
            B) Two
            C) Three
            D) Four

            <details><summary>Answer</summary>

            **D) Four**

            Four is correct.

            </details>
        """)
        questions = parse_questions_text(md, domain_number=2)
        assert len(questions) == 2
        assert questions[0].number == 31
        assert questions[1].number == 32

    def test_source_file_set_to_generated(self):
        questions = parse_questions_text(SAMPLE_QUESTIONS_MD, domain_number=1)
        assert questions[0].source_file == "generated"


class TestSetupExamExisting:
    async def test_existing_exam_returns_ready(self, db):
        """setup_exam returns ready status when the exam already exists in DB."""
        from cert_pepper.db.connection import get_session
        from cert_pepper.mcp.content import setup_exam
        from tests.conftest import seed_certification, seed_domains_for_cert, seed_question

        async with get_session() as session:
            cert_id = await seed_certification(
                session, code="CISSP", name="CISSP Certification", vendor="ISC2"
            )
            await seed_domains_for_cert(
                session, cert_id, [(1, "Security and Risk Management", 15.0)]
            )
            await seed_question(session, domain_number=1, number=1, cert_id=cert_id)

        # Mock ctx — setup_exam should NOT call MCP sampling for an existing exam
        ctx = MagicMock()
        ctx.session = AsyncMock()

        result_str = await setup_exam("CISSP", ctx)
        result = json.loads(result_str)

        assert result["status"] == "ready"
        assert result["exam_code"] == "CISSP"
        assert result["question_count"] == 1
        ctx.session.create_message.assert_not_called()

    async def test_partial_name_match(self, db):
        """setup_exam finds exam by partial name match."""
        from cert_pepper.db.connection import get_session
        from cert_pepper.mcp.content import setup_exam
        from tests.conftest import seed_certification, seed_domains_for_cert

        async with get_session() as session:
            cert_id = await seed_certification(
                session,
                code="SY0-701",
                name="CompTIA Security+ SY0-701",
                vendor="CompTIA",
            )
            await seed_domains_for_cert(
                session, cert_id, [(1, "General Security Concepts", 12.0)]
            )

        ctx = MagicMock()
        ctx.session = AsyncMock()

        result_str = await setup_exam("Security+", ctx)
        result = json.loads(result_str)

        assert result["status"] == "ready"
        assert result["exam_code"] == "SY0-701"
