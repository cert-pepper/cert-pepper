"""Tests for db/connection.py.

Covers:
  - _strip_sql_comments (pure function — the bug it guards against is real)
  - init_db: table creation, seed data, idempotency
  - get_session: commit on success, rollback on exception
"""

from __future__ import annotations

import pytest
from sqlalchemy import text

from cert_pepper.db.connection import (
    _strip_sql_comments,
    get_session,
    init_db,
)


# ---------------------------------------------------------------------------
# _strip_sql_comments — pure function
# ---------------------------------------------------------------------------

class TestStripSqlComments:
    def test_full_line_comment_removed(self):
        sql = "-- this is a comment\nSELECT 1"
        result = _strip_sql_comments(sql)
        assert "--" not in result
        assert "SELECT 1" in result

    def test_inline_comment_removed(self):
        sql = "PRAGMA journal_mode = WAL; -- enable WAL"
        result = _strip_sql_comments(sql)
        assert "--" not in result
        assert "PRAGMA journal_mode = WAL" in result

    def test_semicolon_inside_comment_is_removed(self):
        # This is the exact bug that previously broke init_db:
        # a semicolon inside a -- comment caused the splitter to treat
        # the rest of the line as a new SQL statement.
        sql = "-- SQLite-compatible; PostgreSQL migration path\nPRAGMA foreign_keys = ON"
        result = _strip_sql_comments(sql)
        # After stripping, the first line must be empty (no semicolon surviving)
        first_line = result.split("\n")[0]
        assert ";" not in first_line
        assert "PRAGMA" in result

    def test_sql_without_comments_is_unchanged(self):
        sql = "INSERT INTO users (username) VALUES ('alice');"
        assert _strip_sql_comments(sql) == sql

    def test_empty_string_returns_empty(self):
        assert _strip_sql_comments("") == ""

    def test_only_comment_line_becomes_blank(self):
        sql = "-- nothing here"
        result = _strip_sql_comments(sql)
        assert result.strip() == ""

    def test_multiple_comments_all_removed(self):
        sql = "-- line 1\n-- line 2\nSELECT 2"
        result = _strip_sql_comments(sql)
        assert "--" not in result
        assert "SELECT 2" in result

    def test_preserves_newlines_structure(self):
        sql = "-- comment\nSELECT 1;\nSELECT 2;"
        result = _strip_sql_comments(sql)
        lines = result.split("\n")
        assert len(lines) == 3  # line count preserved


# ---------------------------------------------------------------------------
# init_db — async, uses the `db` fixture from conftest
# ---------------------------------------------------------------------------

class TestInitDb:
    async def test_creates_content_tables(self, db):
        async with get_session() as session:
            for table in ["certifications", "domains", "topics", "questions", "flashcards", "acronyms"]:
                result = await session.execute(
                    text("SELECT name FROM sqlite_master WHERE type='table' AND name=:t"),
                    {"t": table},
                )
                assert result.fetchone() is not None, f"Table '{table}' missing after init_db"

    async def test_creates_progress_tables(self, db):
        async with get_session() as session:
            for table in ["fsrs_cards", "fsrs_reviews", "bkt_skill_states", "question_attempts"]:
                result = await session.execute(
                    text("SELECT name FROM sqlite_master WHERE type='table' AND name=:t"),
                    {"t": table},
                )
                assert result.fetchone() is not None, f"Table '{table}' missing after init_db"

    async def test_creates_ai_cache_table(self, db):
        async with get_session() as session:
            result = await session.execute(
                text("SELECT name FROM sqlite_master WHERE type='table' AND name='ai_explanations'")
            )
            assert result.fetchone() is not None

    async def test_seeds_sy0701_certification(self, db):
        async with get_session() as session:
            result = await session.execute(
                text("SELECT code, vendor FROM certifications WHERE code='SY0-701'")
            )
            row = result.fetchone()
            assert row is not None, "SY0-701 certification not seeded"
            assert row[1] == "CompTIA"

    async def test_seeds_exactly_five_domains(self, db):
        async with get_session() as session:
            result = await session.execute(text("SELECT COUNT(*) FROM domains"))
            assert result.scalar() == 5

    async def test_domain_weights_match_spec(self, db):
        async with get_session() as session:
            result = await session.execute(
                text("SELECT number, weight_pct FROM domains ORDER BY number")
            )
            weights = {row[0]: row[1] for row in result.fetchall()}

        expected = {1: 12.0, 2: 22.0, 3: 18.0, 4: 28.0, 5: 20.0}
        for num, expected_weight in expected.items():
            assert weights[num] == pytest.approx(expected_weight), (
                f"Domain {num} weight wrong: got {weights[num]}, expected {expected_weight}"
            )

    async def test_domain_weights_sum_to_100(self, db):
        async with get_session() as session:
            result = await session.execute(text("SELECT SUM(weight_pct) FROM domains"))
            total = result.scalar()
        assert total == pytest.approx(100.0)

    async def test_seeds_default_user(self, db):
        async with get_session() as session:
            result = await session.execute(
                text("SELECT id FROM users WHERE username='default'")
            )
            assert result.fetchone() is not None, "'default' user not seeded"

    async def test_init_db_is_idempotent(self, db):
        """Calling init_db a second time must not raise or duplicate seed data."""
        await init_db()  # second call
        async with get_session() as session:
            result = await session.execute(text("SELECT COUNT(*) FROM certifications"))
            assert result.scalar() == 1, "init_db created duplicate certifications"

            result = await session.execute(text("SELECT COUNT(*) FROM users WHERE username='default'"))
            assert result.scalar() == 1, "init_db created duplicate users"


# ---------------------------------------------------------------------------
# get_session — transaction behaviour
# ---------------------------------------------------------------------------

class TestGetSession:
    async def test_data_persists_after_successful_block(self, db):
        async with get_session() as session:
            await session.execute(
                text("INSERT INTO users (username) VALUES ('persist_me')")
            )
        # New session reads the committed data
        async with get_session() as session:
            result = await session.execute(
                text("SELECT COUNT(*) FROM users WHERE username='persist_me'")
            )
            assert result.scalar() == 1

    async def test_data_rolled_back_on_exception(self, db):
        with pytest.raises(RuntimeError):
            async with get_session() as session:
                await session.execute(
                    text("INSERT INTO users (username) VALUES ('rollback_me')")
                )
                raise RuntimeError("force rollback")

        async with get_session() as session:
            result = await session.execute(
                text("SELECT COUNT(*) FROM users WHERE username='rollback_me'")
            )
            assert result.scalar() == 0, "Rolled-back insert should not be visible"

    async def test_multiple_sessions_are_independent(self, db):
        """Two concurrent sessions each see their own uncommitted state."""
        from cert_pepper.db.connection import get_session_factory

        factory = get_session_factory()
        async with factory() as s1:
            await s1.execute(text("INSERT INTO users (username) VALUES ('session_a')"))
            # Before s1 commits, s2 should not see 'session_a'
            async with factory() as s2:
                result = await s2.execute(
                    text("SELECT COUNT(*) FROM users WHERE username='session_a'")
                )
                # SQLite serializes writes; both see 0 before commit
                assert result.scalar() == 0
            await s1.commit()

        # After s1 commits, a fresh session sees it
        async with get_session() as session:
            result = await session.execute(
                text("SELECT COUNT(*) FROM users WHERE username='session_a'")
            )
            assert result.scalar() == 1
