"""Tests for setup_exam MCP tool and parse_questions_text."""

from __future__ import annotations

import json
import textwrap
from unittest.mock import AsyncMock, MagicMock, patch

import httpx
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


# ── helpers for mocking httpx AsyncClient ──────────────────────────────────────

def _make_reddit_json(posts: list[dict]) -> dict:
    """Build a minimal Reddit JSON API response with the given posts."""
    return {
        "data": {
            "children": [
                {"data": {"title": p["title"], "selftext": p["selftext"], "score": p["score"]}}
                for p in posts
            ]
        }
    }


def _make_mock_client(json_return_value: dict) -> MagicMock:
    """Return a mock httpx.AsyncClient that returns json_return_value on GET."""
    mock_resp = MagicMock()
    mock_resp.raise_for_status = MagicMock()
    mock_resp.json.return_value = json_return_value

    mock_client = AsyncMock()
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=False)
    mock_client.get = AsyncMock(return_value=mock_resp)
    return mock_client


class TestFetchRedditExcerpts:
    async def test_success_returns_excerpt_list(self):
        from cert_pepper.mcp.content import _fetch_reddit_excerpts

        posts = [
            {"title": "Passed CISSP!", "selftext": "Focus on risk management.", "score": 50},
            {"title": "Tips for CISSP", "selftext": "BCP is huge on the exam.", "score": 30},
        ]
        mock_client = _make_mock_client(_make_reddit_json(posts))

        with patch("cert_pepper.mcp.content.httpx.AsyncClient", return_value=mock_client):
            result = await _fetch_reddit_excerpts("CISSP", "ISC2")

        assert isinstance(result, list)
        assert len(result) > 0
        assert any("CISSP" in excerpt or "risk" in excerpt for excerpt in result)

    async def test_network_error_returns_empty_list(self):
        from cert_pepper.mcp.content import _fetch_reddit_excerpts

        mock_client = AsyncMock()
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=False)
        mock_client.get = AsyncMock(
            side_effect=httpx.RequestError("connection refused", request=MagicMock())
        )

        with patch("cert_pepper.mcp.content.httpx.AsyncClient", return_value=mock_client):
            result = await _fetch_reddit_excerpts("CISSP", "ISC2")

        assert result == []

    async def test_malformed_json_returns_empty_list(self):
        from cert_pepper.mcp.content import _fetch_reddit_excerpts

        # JSON without expected structure
        mock_client = _make_mock_client({"unexpected": "structure"})

        with patch("cert_pepper.mcp.content.httpx.AsyncClient", return_value=mock_client):
            result = await _fetch_reddit_excerpts("CISSP", "ISC2")

        assert result == []

    async def test_http_error_returns_empty_list(self):
        from cert_pepper.mcp.content import _fetch_reddit_excerpts

        mock_resp = MagicMock()
        mock_resp.raise_for_status = MagicMock(
            side_effect=httpx.HTTPStatusError(
                "429 Too Many Requests",
                request=MagicMock(),
                response=MagicMock(),
            )
        )

        mock_client = AsyncMock()
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=False)
        mock_client.get = AsyncMock(return_value=mock_resp)

        with patch("cert_pepper.mcp.content.httpx.AsyncClient", return_value=mock_client):
            result = await _fetch_reddit_excerpts("CISSP", "ISC2")

        assert result == []

    async def test_empty_children_returns_empty_list(self):
        from cert_pepper.mcp.content import _fetch_reddit_excerpts

        mock_client = _make_mock_client(_make_reddit_json([]))

        with patch("cert_pepper.mcp.content.httpx.AsyncClient", return_value=mock_client):
            result = await _fetch_reddit_excerpts("CISSP", "ISC2")

        assert result == []

    async def test_low_score_posts_excluded(self):
        from cert_pepper.mcp.content import _fetch_reddit_excerpts

        posts = [
            {"title": "Spam post", "selftext": "Buy my course!", "score": 1},
            {"title": "Good post", "selftext": "Domain 1 is heavily tested.", "score": 20},
        ]
        mock_client = _make_mock_client(_make_reddit_json(posts))

        with patch("cert_pepper.mcp.content.httpx.AsyncClient", return_value=mock_client):
            result = await _fetch_reddit_excerpts("CISSP", "ISC2")

        assert len(result) == 1
        assert "Domain 1" in result[0]

    async def test_removed_deleted_posts_excluded(self):
        from cert_pepper.mcp.content import _fetch_reddit_excerpts

        posts = [
            {"title": "Removed post", "selftext": "[removed]", "score": 100},
            {"title": "Deleted post", "selftext": "[deleted]", "score": 100},
            {"title": "Good post", "selftext": "Study access controls.", "score": 50},
        ]
        mock_client = _make_mock_client(_make_reddit_json(posts))

        with patch("cert_pepper.mcp.content.httpx.AsyncClient", return_value=mock_client):
            result = await _fetch_reddit_excerpts("CISSP", "ISC2")

        assert len(result) == 1
        assert "access" in result[0]


class TestBuildResearchContext:
    async def test_returns_synthesis_when_excerpts_available(self):
        from cert_pepper.mcp.content import _build_research_context

        excerpts = ["Passed CISSP: Focus on risk management.", "Tips: BCP is huge."]

        sampling_result = MagicMock()
        sampling_result.content = MagicMock()
        sampling_result.content.text = "- Risk management is critical\n- BCP tested heavily"

        ctx = MagicMock()
        ctx.session = AsyncMock()
        ctx.session.create_message = AsyncMock(return_value=sampling_result)

        with patch(
            "cert_pepper.mcp.content._fetch_reddit_excerpts", return_value=excerpts
        ):
            result = await _build_research_context("CISSP", "ISC2", ctx)

        assert isinstance(result, str)
        assert len(result) > 0
        ctx.session.create_message.assert_called_once()

    async def test_returns_empty_string_when_no_excerpts(self):
        from cert_pepper.mcp.content import _build_research_context

        ctx = MagicMock()
        ctx.session = AsyncMock()

        with patch("cert_pepper.mcp.content._fetch_reddit_excerpts", return_value=[]):
            result = await _build_research_context("CISSP", "ISC2", ctx)

        assert result == ""
        ctx.session.create_message.assert_not_called()

    async def test_returns_empty_string_when_sampling_fails(self):
        from cert_pepper.mcp.content import _build_research_context

        ctx = MagicMock()
        ctx.session = AsyncMock()
        ctx.session.create_message = AsyncMock(side_effect=RuntimeError("sampling failed"))

        with patch(
            "cert_pepper.mcp.content._fetch_reddit_excerpts",
            return_value=["Some excerpt: content here."],
        ):
            result = await _build_research_context("CISSP", "ISC2", ctx)

        assert result == ""

    def test_research_context_injected_into_questions_user_prompt(self):
        from cert_pepper.mcp.content import _QUESTIONS_USER

        research_context = (
            "\nCommunity exam insights (incorporate into question difficulty and distractors):\n"
            "- PKI tested heavily\n"
        )
        rendered = _QUESTIONS_USER.format(
            n=30,
            start=1,
            end=30,
            exam_name="CISSP",
            domain_number=1,
            domain_name="Security and Risk Management",
            weight_pct=15.0,
            research_context=research_context,
        )
        assert "- PKI tested heavily" in rendered

    def test_research_context_empty_string_renders_cleanly(self):
        from cert_pepper.mcp.content import _QUESTIONS_USER

        rendered = _QUESTIONS_USER.format(
            n=30,
            start=1,
            end=30,
            exam_name="CISSP",
            domain_number=1,
            domain_name="Security and Risk Management",
            weight_pct=15.0,
            research_context="",
        )
        assert "CISSP" in rendered
        assert "Security and Risk Management" in rendered
