"""Shared pytest fixtures for cert-pepper tests.

The primary fixture is `db`, which:
  - Patches DB_PATH to an isolated per-test SQLite file
  - Resets the SQLAlchemy engine singleton so it picks up the new path
  - Initializes the schema and seeds the default certification/domains/user
  - Disposes and resets the singleton after the test

All tests that touch the database must use `db` (or a fixture that depends on it).
Tests for pure functions do not need it.
"""

from __future__ import annotations

import pytest
from pathlib import Path
from sqlalchemy import text

import cert_pepper.db.connection as _conn_module


@pytest.fixture
async def db(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """
    Provide a fresh, isolated SQLite database initialized with the full schema.

    Yields the path to the database file.
    """
    db_path = tmp_path / "test.db"

    # Patch DB_PATH so get_settings() / get_engine() use the temp file.
    # Env vars take precedence over .env files in Pydantic Settings v2.
    monkeypatch.setenv("DB_PATH", str(db_path))

    # Reset singletons so get_engine() creates a new one pointing to db_path.
    _conn_module._engine = None
    _conn_module._session_factory = None

    from cert_pepper.db.connection import init_db
    await init_db()

    yield db_path

    # Dispose the engine and clear singletons for the next test.
    if _conn_module._engine is not None:
        await _conn_module._engine.dispose()
    _conn_module._engine = None
    _conn_module._session_factory = None


# ---------------------------------------------------------------------------
# Data-seeding helpers (used by multiple test modules)
# ---------------------------------------------------------------------------

async def seed_question(
    session,
    domain_number: int = 4,
    number: int = 1,
    stem: str = "Test question?",
    correct_answer: str = "A",
) -> int:
    """Insert a minimal question and return its id."""
    result = await session.execute(
        text("SELECT id FROM domains WHERE number = :n"),
        {"n": domain_number},
    )
    domain_id = result.scalar()
    assert domain_id is not None, f"Domain {domain_number} not found — was init_db called?"

    await session.execute(
        text("""
            INSERT INTO questions
                (domain_id, number, stem, option_a, option_b, option_c, option_d, correct_answer)
            VALUES (:did, :num, :stem, 'Option A', 'Option B', 'Option C', 'Option D', :ans)
        """),
        {"did": domain_id, "num": number, "stem": stem, "ans": correct_answer},
    )
    result = await session.execute(text("SELECT last_insert_rowid()"))
    return result.scalar()


async def seed_attempt(
    session,
    user_id: int,
    question_id: int,
    session_id: int,
    is_correct: bool = True,
) -> None:
    """Insert a question_attempt record."""
    await session.execute(
        text("""
            INSERT INTO question_attempts
                (session_id, user_id, question_id, selected_answer, is_correct)
            VALUES (:sid, :uid, :qid, 'A', :correct)
        """),
        {
            "sid": session_id,
            "uid": user_id,
            "qid": question_id,
            "correct": 1 if is_correct else 0,
        },
    )


async def seed_session(session, user_id: int) -> int:
    """Insert a study_session and return its id."""
    await session.execute(
        text("INSERT INTO study_sessions (user_id, session_type) VALUES (:uid, 'study')"),
        {"uid": user_id},
    )
    result = await session.execute(text("SELECT last_insert_rowid()"))
    return result.scalar()


async def get_user_id(session) -> int:
    """Return the default user's id."""
    result = await session.execute(
        text("SELECT id FROM users WHERE username='default' LIMIT 1")
    )
    return result.scalar()
