"""Tests for pregenerate module — verifies parameterized SQL queries."""

from __future__ import annotations

import ast
import inspect
import textwrap


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
