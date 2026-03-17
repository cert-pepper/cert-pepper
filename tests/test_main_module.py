"""Tests for cert_pepper.__main__ module."""

from cert_pepper.__main__ import app


def test_main_module_exposes_app() -> None:
    """The __main__ module must expose the Typer app for `python -m cert_pepper`."""
    from typer import Typer

    assert isinstance(app, Typer)
