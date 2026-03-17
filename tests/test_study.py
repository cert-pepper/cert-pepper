"""Tests for cert_pepper/cli/study.py."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from cert_pepper.cli.study import run_study_session


class TestScreenClearBetweenQuestions:
    """Console should be cleared before each question except the first."""

    async def test_clear_called_between_questions(self, db):
        """console.clear() is called count-1 times (skipped on first question)."""
        from cert_pepper.db.connection import get_session
        from tests.conftest import get_user_id, seed_question

        async with get_session() as session:
            user_id = await get_user_id(session)
            q_id = await seed_question(session, domain_number=1, number=1)

        mock_q = MagicMock()
        mock_q.stem = "Test stem?"
        mock_q.correct_answer = "A"
        mock_q.domain_id = 1
        mock_q.domain_number = 1
        mock_q.explanation = "Some explanation"
        mock_q.options_dict.return_value = {
            "A": "Option A", "B": "Option B", "C": "Option C", "D": "Option D",
        }
        mock_q.get_option.return_value = "Option A"

        with (
            patch("cert_pepper.cli.study.selector.select_question", new_callable=AsyncMock, return_value=q_id),
            patch("cert_pepper.cli.study.get_question", new_callable=AsyncMock, return_value=mock_q),
            patch("cert_pepper.cli.study.get_answer_from_user", return_value=("A", False)),
            patch("cert_pepper.cli.study.display_question"),
            patch("cert_pepper.cli.study.get_fsrs_rating", return_value=3),
            patch("cert_pepper.cli.study.get_or_create_fsrs_card", new_callable=AsyncMock),
            patch("cert_pepper.cli.study.save_fsrs_card", new_callable=AsyncMock),
            patch("cert_pepper.cli.study.update_bkt", new_callable=AsyncMock),
            patch("cert_pepper.cli.study.console") as mock_console,
        ):
            await run_study_session(count=3)
            assert mock_console.clear.call_count == 2  # skipped on first, called before Q2 and Q3


class TestQuitMidQuestion:
    """Regression tests for the 'q' quit path in run_study_session."""

    async def test_quit_mid_question_no_unbound_error(self, db):
        """Typing 'q' mid-question must not raise UnboundLocalError.

        Previously a broken while/else pattern left `answer` unresolved when
        KeyboardInterrupt was raised by get_answer_from_user, causing
        UnboundLocalError on the line `is_correct = answer == q.correct_answer`.
        """
        mock_q = MagicMock()
        mock_q.stem = "Test stem?"
        mock_q.correct_answer = "A"
        mock_q.domain_id = 1
        mock_q.domain_number = 1
        mock_q.explanation = None
        mock_q.options_dict.return_value = {
            "A": "Option A", "B": "Option B", "C": "Option C", "D": "Option D"
        }

        with (
            patch("cert_pepper.cli.study.selector.select_question", new_callable=AsyncMock, return_value=1),
            patch("cert_pepper.cli.study.get_question", new_callable=AsyncMock, return_value=mock_q),
            patch("cert_pepper.cli.study.get_answer_from_user", side_effect=KeyboardInterrupt),
            patch("cert_pepper.cli.study.display_question"),
            patch("cert_pepper.cli.study.get_default_user_id", new_callable=AsyncMock, return_value=1),
        ):
            # Must complete without raising UnboundLocalError (or any other error)
            await run_study_session(count=3)
