"""Tests for pregenerate module — verifies parameterized SQL queries."""

from __future__ import annotations

import inspect
from unittest.mock import AsyncMock, patch

from cert_pepper.db.connection import get_session
from tests.conftest import (
    seed_certification,
    seed_domains_for_cert,
    seed_question,
)


class TestPregenerateSQL:
    """Verify pregenerate uses parameterized queries, not f-string interpolation."""

    def test_no_fstring_sql_injection(self):
        """The domain filter query must use :domain_filter param, not f-string."""
        from cert_pepper.cli.pregenerate import run_pregenerate

        source = inspect.getsource(run_pregenerate)
        # Must not interpolate domain_filter directly into SQL
        assert "f\"AND d.number = {domain_filter}\"" not in source
        assert "f'AND d.number = {domain_filter}'" not in source

    def test_domain_clause_uses_named_param(self):
        """The domain filter must use :domain_filter named parameter."""
        from cert_pepper.cli.pregenerate import run_pregenerate

        source = inspect.getsource(run_pregenerate)
        assert ":domain_filter" in source


class TestPregenerateExamCodePerQuestion:
    """Each question's exam_code must be derived from its own certification —
    a single user-supplied --exam would poison the shared cache when both
    exams are ingested."""

    async def test_exam_code_derived_per_question(self, db):
        from cert_pepper.cli.pregenerate import run_pregenerate

        async with get_session() as session:
            sy_id = await seed_certification(session, code="SY0-701", name="Security+")
            cy_id = await seed_certification(session, code="CY0-001", name="SecAI+")
            await seed_domains_for_cert(session, sy_id, [(1, "D1", 100.0)])
            await seed_domains_for_cert(session, cy_id, [(1, "D1", 100.0)])
            await seed_question(session, domain_number=1, number=1, cert_id=sy_id)
            await seed_question(session, domain_number=1, number=2, cert_id=cy_id)

        captured: list[str] = []

        async def fake_get_explanation(_session, _q, _wrong, exam_code):
            captured.append(exam_code)
            return "ok"

        with patch(
            "cert_pepper.ai.explainer.get_explanation",
            AsyncMock(side_effect=fake_get_explanation),
        ):
            await run_pregenerate()

        # Two questions × three wrong answers each = six calls.
        # Three should be SY0-701, three should be CY0-001 — never mixed.
        assert captured.count("SY0-701") == 3
        assert captured.count("CY0-001") == 3
