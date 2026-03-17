"""Tests for exam CLI helpers."""
import threading
import time
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from cert_pepper.cli.exam import _timer_thread, format_time, run_exam


def test_format_time():
    assert format_time(0) == "00:00"
    assert format_time(90) == "01:30"
    assert format_time(3661) == "61:01"


class TestScreenClearBetweenQuestions:
    """Console should be cleared before each question except the first."""

    async def test_clear_called_between_exam_questions(self, db):
        """console.clear() is called for questions after the first."""
        from cert_pepper.db.connection import get_session
        from tests.conftest import get_user_id, seed_question

        async with get_session() as session:
            user_id = await get_user_id(session)
            q_ids = [
                await seed_question(session, domain_number=1, number=n)
                for n in range(1, 4)
            ]

        mock_q = MagicMock()
        mock_q.stem = "Test stem?"
        mock_q.correct_answer = "A"
        mock_q.domain_id = 1
        mock_q.domain_number = 1
        mock_q.options_dict.return_value = {
            "A": "Option A", "B": "Option B", "C": "Option C", "D": "Option D",
        }

        with (
            patch("cert_pepper.cli.exam.get_question", new_callable=AsyncMock, return_value=mock_q),
            patch("cert_pepper.cli.exam.selector.select_exam_questions", new_callable=AsyncMock, return_value=q_ids),
            patch("cert_pepper.cli.exam.count_unseen_questions", new_callable=AsyncMock, return_value=(3, 3)),
            patch("cert_pepper.cli.exam.Prompt.ask", side_effect=["Y", "A", "A", "A"]),
            patch("cert_pepper.cli.exam.signal.signal"),
            patch("cert_pepper.cli.exam.signal.alarm"),
            patch("cert_pepper.cli.exam.console") as mock_console,
        ):
            mock_console.width = 80
            await run_exam(total_questions=3, time_limit_minutes=5)
            assert mock_console.clear.call_count == 2  # skipped on first (i==1), called for i==2 and i==3


def test_timer_thread_stops_on_event():
    stop = threading.Event()
    t = threading.Thread(
        target=_timer_thread,
        args=(time.time(), 300.0, stop),
        daemon=True,
    )
    t.start()
    stop.set()
    t.join(timeout=2.0)
    assert not t.is_alive()
