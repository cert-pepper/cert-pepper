"""Tests for exam CLI helpers."""
import threading
import time

from cert_pepper.cli.exam import _timer_thread, format_time


def test_format_time():
    assert format_time(0) == "00:00"
    assert format_time(90) == "01:30"
    assert format_time(3661) == "61:01"


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
