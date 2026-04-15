"""Tests for the flashcard review session."""

from __future__ import annotations

from unittest.mock import patch

from tests.conftest import (
    seed_certification,
    seed_domains_for_cert,
    seed_flashcard,
)


class TestFlashcardSession:
    async def test_run_flashcard_session_shows_all_cards(self, db):
        """Three cards → three panel prints plus one completion print."""
        from cert_pepper.cli.flashcards import run_flashcard_session

        from cert_pepper.db.connection import get_session

        async with get_session() as session:
            cert_id = await seed_certification(session, code="FC01")
            await seed_domains_for_cert(session, cert_id)
            await seed_flashcard(session, front="Term 1", back="Def 1", cert_id=cert_id)
            await seed_flashcard(session, front="Term 2", back="Def 2", cert_id=cert_id)
            await seed_flashcard(session, front="Term 3", back="Def 3", cert_id=cert_id)

        printed = []
        with patch("cert_pepper.cli.flashcards.Prompt.ask", return_value=""):
            with patch("cert_pepper.cli.flashcards.console.print",
                       side_effect=printed.append):
                await run_flashcard_session(exam_code="FC01")

        # 3 panel prints + 1 completion message
        assert len(printed) == 4

    async def test_run_flashcard_session_domain_filter(self, db):
        """Only cards from the requested domain are shown."""
        from cert_pepper.cli.flashcards import run_flashcard_session

        from cert_pepper.db.connection import get_session

        async with get_session() as session:
            cert_id = await seed_certification(session, code="FC02")
            await seed_domains_for_cert(session, cert_id, [(1, "D1", 50.0), (2, "D2", 50.0)])
            await seed_flashcard(session, front="D1 Term", back="D1 Def",
                                 domain_number=1, cert_id=cert_id)
            await seed_flashcard(session, front="D2 Term", back="D2 Def",
                                 domain_number=2, cert_id=cert_id)

        printed = []
        with patch("cert_pepper.cli.flashcards.Prompt.ask", return_value=""):
            with patch("cert_pepper.cli.flashcards.console.print",
                       side_effect=printed.append):
                await run_flashcard_session(exam_code="FC02", domain=1)

        # 1 panel + 1 completion
        assert len(printed) == 2
        panel_text = str(printed[0].renderable)
        assert "D1 Term" in panel_text
        assert "D2 Term" not in panel_text

    async def test_run_flashcard_session_category_filter(self, db):
        """Only cards from the requested category are shown."""
        from cert_pepper.cli.flashcards import run_flashcard_session

        from cert_pepper.db.connection import get_session

        async with get_session() as session:
            cert_id = await seed_certification(session, code="FC03")
            await seed_domains_for_cert(session, cert_id)
            await seed_flashcard(session, front="Cat A Term", back="Cat A Def",
                                 category="Alpha", cert_id=cert_id)
            await seed_flashcard(session, front="Cat B Term", back="Cat B Def",
                                 category="Beta", cert_id=cert_id)

        printed = []
        with patch("cert_pepper.cli.flashcards.Prompt.ask", return_value=""):
            with patch("cert_pepper.cli.flashcards.console.print",
                       side_effect=printed.append):
                await run_flashcard_session(exam_code="FC03", category="Alpha")

        # 1 panel + 1 completion
        assert len(printed) == 2
        panel_text = str(printed[0].renderable)
        assert "Cat A Term" in panel_text
        assert "Cat B Term" not in panel_text

    async def test_run_flashcard_session_count_cap(self, db):
        """count=2 with 5 cards shows only 2 panels."""
        from cert_pepper.cli.flashcards import run_flashcard_session

        from cert_pepper.db.connection import get_session

        async with get_session() as session:
            cert_id = await seed_certification(session, code="FC04")
            await seed_domains_for_cert(session, cert_id)
            for i in range(5):
                await seed_flashcard(session, front=f"Term {i}", back=f"Def {i}",
                                     cert_id=cert_id)

        printed = []
        with patch("cert_pepper.cli.flashcards.Prompt.ask", return_value=""):
            with patch("cert_pepper.cli.flashcards.console.print",
                       side_effect=printed.append):
                await run_flashcard_session(exam_code="FC04", count=2)

        # 2 panels + 1 completion
        assert len(printed) == 3

    async def test_run_flashcard_session_no_cards_exits_cleanly(self, db):
        """No flashcards for the cert → single yellow warning, no crash."""
        from cert_pepper.cli.flashcards import run_flashcard_session

        from cert_pepper.db.connection import get_session

        async with get_session() as session:
            cert_id = await seed_certification(session, code="FC05")
            await seed_domains_for_cert(session, cert_id)
            # no flashcards seeded

        printed = []
        with patch("cert_pepper.cli.flashcards.console.print",
                   side_effect=printed.append):
            await run_flashcard_session(exam_code="FC05")

        assert len(printed) == 1
        assert "No flashcards" in str(printed[0])
