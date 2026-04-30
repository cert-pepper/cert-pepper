"""Tests for the flashcard review session."""

from __future__ import annotations

from unittest.mock import patch

import pytest
from rich.panel import Panel

from cert_pepper.db.connection import get_session
from tests.conftest import (
    seed_certification,
    seed_domains_for_cert,
    seed_flashcard,
)


def _panel_texts(printed: list) -> list[str]:
    """Return text from each Panel in order — stable across cosmetic prints."""
    return [str(p.renderable) for p in printed if isinstance(p, Panel)]


def _all_panel_text(printed: list) -> str:
    """Concatenate all panel renderables for substring assertions."""
    return "\n".join(_panel_texts(printed))


class TestLastCardWaitsForKeypress:
    """The final card's reveal panel must wait for a keypress; otherwise
    the panel renders and then immediately gets buried by the Done line."""

    async def test_flip_mode_waits_on_last_answer_side(self, db):
        from cert_pepper.cli.flashcards import run_flashcard_session

        async with get_session() as session:
            cert_id = await seed_certification(session, code="FCL1")
            await seed_domains_for_cert(session, cert_id)
            for i in range(3):
                await seed_flashcard(
                    session, front=f"T{i}", back=f"D{i}", cert_id=cert_id
                )

        with patch(
            "cert_pepper.cli.flashcards._getkey", return_value=""
        ) as mock_getkey:
            await run_flashcard_session(exam_code="FCL1")

        # 3 cards × 2 keypresses (question side + answer side) each.
        assert mock_getkey.call_count == 6

    async def test_show_answer_mode_waits_on_last_card(self, db):
        from cert_pepper.cli.flashcards import run_flashcard_session

        async with get_session() as session:
            cert_id = await seed_certification(session, code="FCL2")
            await seed_domains_for_cert(session, cert_id)
            for i in range(3):
                await seed_flashcard(
                    session, front=f"T{i}", back=f"D{i}", cert_id=cert_id
                )

        with patch(
            "cert_pepper.cli.flashcards._getkey", return_value=""
        ) as mock_getkey:
            await run_flashcard_session(exam_code="FCL2", show_answer=True)

        # 3 cards × 1 keypress each (combined panel).
        assert mock_getkey.call_count == 3


class TestCommandRegistration:
    """The CLI command is plural — `flashcards` — to match the content
    directory and PR documentation."""

    def test_flashcards_command_registered(self):
        from cert_pepper.cli.main import app

        names = {cmd.name for cmd in app.registered_commands}
        assert "flashcards" in names
        assert "flashcard" not in names


class TestGetKey:
    """Direct tests for _getkey — patch click.getchar, not _getkey itself.

    Earlier tests stubbed _getkey, hiding a bytes/str mismatch in _QUIT_KEYS.
    """

    @pytest.mark.parametrize("ch", ["q", "Q", "\x1b"])
    def test_quit_keys_return_q(self, ch):
        from cert_pepper.cli.flashcards import _getkey

        with patch("cert_pepper.cli.flashcards.click.getchar", return_value=ch):
            assert _getkey() == "q"

    @pytest.mark.parametrize("ch", ["", "\r", "\n", "a"])
    def test_non_quit_keys_return_empty(self, ch):
        from cert_pepper.cli.flashcards import _getkey

        with patch("cert_pepper.cli.flashcards.click.getchar", return_value=ch):
            assert _getkey() == ""


class TestFlashcardSession:
    async def test_run_flashcard_session_shows_all_cards(self, db):
        """Every seeded card's content is visible across the rendered panels."""
        from cert_pepper.cli.flashcards import run_flashcard_session

        async with get_session() as session:
            cert_id = await seed_certification(session, code="FC01")
            await seed_domains_for_cert(session, cert_id)
            await seed_flashcard(session, front="Term 1", back="Def 1", cert_id=cert_id)
            await seed_flashcard(session, front="Term 2", back="Def 2", cert_id=cert_id)
            await seed_flashcard(session, front="Term 3", back="Def 3", cert_id=cert_id)

        printed = []
        with patch("cert_pepper.cli.flashcards._getkey", return_value=""):
            with patch("cert_pepper.cli.flashcards.console.print",
                       side_effect=printed.append):
                await run_flashcard_session(exam_code="FC01")

        text = _all_panel_text(printed)
        for n in (1, 2, 3):
            assert f"Term {n}" in text
            assert f"Def {n}" in text

    async def test_run_flashcard_session_domain_filter(self, db):
        """Only cards from the requested domain are rendered."""
        from cert_pepper.cli.flashcards import run_flashcard_session

        async with get_session() as session:
            cert_id = await seed_certification(session, code="FC02")
            await seed_domains_for_cert(session, cert_id, [(1, "D1", 50.0), (2, "D2", 50.0)])
            await seed_flashcard(session, front="D1 Term", back="D1 Def",
                                 domain_number=1, cert_id=cert_id)
            await seed_flashcard(session, front="D2 Term", back="D2 Def",
                                 domain_number=2, cert_id=cert_id)

        printed = []
        with patch("cert_pepper.cli.flashcards._getkey", return_value=""):
            with patch("cert_pepper.cli.flashcards.console.print",
                       side_effect=printed.append):
                await run_flashcard_session(exam_code="FC02", domain=1)

        text = _all_panel_text(printed)
        assert "D1 Def" in text
        assert "D2 Def" not in text

    async def test_run_flashcard_session_category_filter(self, db):
        """Only cards from the requested category are rendered."""
        from cert_pepper.cli.flashcards import run_flashcard_session

        async with get_session() as session:
            cert_id = await seed_certification(session, code="FC03")
            await seed_domains_for_cert(session, cert_id)
            await seed_flashcard(session, front="Cat A Term", back="Cat A Def",
                                 category="Alpha", cert_id=cert_id)
            await seed_flashcard(session, front="Cat B Term", back="Cat B Def",
                                 category="Beta", cert_id=cert_id)

        printed = []
        with patch("cert_pepper.cli.flashcards._getkey", return_value=""):
            with patch("cert_pepper.cli.flashcards.console.print",
                       side_effect=printed.append):
                await run_flashcard_session(exam_code="FC03", category="Alpha")

        text = _all_panel_text(printed)
        assert "Cat A Def" in text
        assert "Cat B Def" not in text

    async def test_run_flashcard_session_count_cap(self, db):
        """count=2 with 5 cards shows only 2 distinct cards."""
        from cert_pepper.cli.flashcards import run_flashcard_session

        async with get_session() as session:
            cert_id = await seed_certification(session, code="FC04")
            await seed_domains_for_cert(session, cert_id)
            for i in range(5):
                await seed_flashcard(session, front=f"Term {i}", back=f"Def {i}",
                                     cert_id=cert_id)

        printed = []
        with patch("cert_pepper.cli.flashcards._getkey", return_value=""):
            with patch("cert_pepper.cli.flashcards.console.print",
                       side_effect=printed.append):
                await run_flashcard_session(exam_code="FC04", count=2)

        text = _all_panel_text(printed)
        shown = sum(1 for i in range(5) if f"Def {i}" in text)
        assert shown == 2

    async def test_run_flashcard_session_no_cards_exits_cleanly(self, db):
        """No flashcards for the cert → single yellow warning, no crash."""
        from cert_pepper.cli.flashcards import run_flashcard_session

        async with get_session() as session:
            cert_id = await seed_certification(session, code="FC05")
            await seed_domains_for_cert(session, cert_id)

        printed = []
        with patch("cert_pepper.cli.flashcards.console.print",
                   side_effect=printed.append):
            await run_flashcard_session(exam_code="FC05")

        assert len(printed) == 1
        assert "No flashcards" in str(printed[0])

    async def test_show_answer_single_panel_per_card(self, db):
        """show_answer=True renders one combined panel per card (front+back together)."""
        from cert_pepper.cli.flashcards import run_flashcard_session

        async with get_session() as session:
            cert_id = await seed_certification(session, code="FC08")
            await seed_domains_for_cert(session, cert_id)
            await seed_flashcard(session, front="Term A", back="Def A", cert_id=cert_id)
            await seed_flashcard(session, front="Term B", back="Def B", cert_id=cert_id)
            await seed_flashcard(session, front="Term C", back="Def C", cert_id=cert_id)

        printed = []
        with patch("cert_pepper.cli.flashcards._getkey", return_value=""):
            with patch("cert_pepper.cli.flashcards.console.print",
                       side_effect=printed.append):
                await run_flashcard_session(exam_code="FC08", show_answer=True)

        panels = _panel_texts(printed)
        # 3 cards × 1 combined panel each, and each panel holds front+back together.
        assert len(panels) == 3
        for panel_text in panels:
            assert any(
                f"Term {ch}" in panel_text and f"Def {ch}" in panel_text
                for ch in ("A", "B", "C")
            )

    async def test_show_answer_panel_contains_both_sides(self, db):
        """show_answer panel includes both definition and term."""
        from cert_pepper.cli.flashcards import run_flashcard_session

        async with get_session() as session:
            cert_id = await seed_certification(session, code="FC09")
            await seed_domains_for_cert(session, cert_id)
            await seed_flashcard(
                session,
                front="CIA Triad",
                back="Confidentiality Integrity Availability",
                cert_id=cert_id,
            )

        printed = []
        with patch("cert_pepper.cli.flashcards._getkey", return_value=""):
            with patch("cert_pepper.cli.flashcards.console.print",
                       side_effect=printed.append):
                await run_flashcard_session(exam_code="FC09", show_answer=True)

        panel_text = str(printed[0].renderable)
        assert "Confidentiality Integrity Availability" in panel_text
        assert "CIA Triad" in panel_text

