"""Tests for cert_pepper/cli/study.py."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from cert_pepper.cli.study import run_study_session


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
