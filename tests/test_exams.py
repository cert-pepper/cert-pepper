"""Tests for cert_pepper/db/exams.py — resolve_cert_id and get_cert_id_for_session."""

from __future__ import annotations

import pytest
from sqlalchemy import text

from cert_pepper.db.connection import get_session
from cert_pepper.db.exams import resolve_cert_id, get_cert_id_for_session

from tests.conftest import seed_certification, seed_domains_for_cert, get_cert_id


class TestResolveCertId:
    async def test_auto_single_cert_resolves(self, db):
        """With exactly one certification in DB, resolve_cert_id(None) returns its id."""
        async with get_session() as session:
            cert_id = await get_cert_id(session, "SY0-701")
            result = await resolve_cert_id(session)
        assert result == cert_id

    async def test_resolve_by_code(self, db):
        """resolve_cert_id('SY0-701') returns the correct id."""
        async with get_session() as session:
            cert_id = await get_cert_id(session, "SY0-701")
            result = await resolve_cert_id(session, "SY0-701")
        assert result == cert_id

    async def test_unknown_code_raises_value_error(self, db):
        """resolve_cert_id('NONEXISTENT') raises ValueError."""
        async with get_session() as session:
            with pytest.raises(ValueError, match="NONEXISTENT"):
                await resolve_cert_id(session, "NONEXISTENT")

    async def test_multiple_certs_no_code_raises(self, db):
        """With multiple certs and no exam_code, raises ValueError listing codes."""
        async with get_session() as session:
            await seed_certification(session, "AWS-SAA", "AWS Solutions Architect")
            await session.commit()

        async with get_session() as session:
            with pytest.raises(ValueError, match="Multiple exams"):
                await resolve_cert_id(session)

    async def test_multiple_certs_with_code_resolves_correctly(self, db):
        """With multiple certs, specifying exam_code returns the right one."""
        async with get_session() as session:
            aws_id = await seed_certification(session, "AWS-SAA", "AWS Solutions Architect")
            await session.commit()

        async with get_session() as session:
            result = await resolve_cert_id(session, "AWS-SAA")
        assert result == aws_id

    async def test_zero_certs_raises_value_error(self, tmp_path, monkeypatch):
        """With no certs in DB, raises ValueError."""
        import cert_pepper.db.connection as _conn_module

        db_path = tmp_path / "empty.db"
        monkeypatch.setenv("DB_PATH", str(db_path))
        _conn_module._engine = None
        _conn_module._session_factory = None

        from cert_pepper.db.connection import get_engine, init_db
        engine = get_engine()

        # Create minimal schema without seeding any certifications
        async with engine.begin() as conn:
            await conn.execute(text("CREATE TABLE IF NOT EXISTS certifications (id INTEGER PRIMARY KEY, code TEXT UNIQUE, name TEXT, vendor TEXT)"))
            await conn.execute(text("CREATE TABLE IF NOT EXISTS study_sessions (id INTEGER PRIMARY KEY, user_id INTEGER, session_type TEXT, certification_id INTEGER)"))

        from cert_pepper.db.connection import get_session as gs
        async with gs() as session:
            with pytest.raises(ValueError, match="No exams found"):
                await resolve_cert_id(session)

        await engine.dispose()
        _conn_module._engine = None
        _conn_module._session_factory = None


class TestGetCertIdForSession:
    async def test_returns_cert_id_for_session(self, db):
        """get_cert_id_for_session returns the certification_id stored in study_sessions."""
        async with get_session() as session:
            cert_id = await get_cert_id(session, "SY0-701")
            await session.execute(
                text("INSERT INTO study_sessions (user_id, session_type, certification_id) VALUES (1, 'study', :cid)"),
                {"cid": cert_id},
            )
            result = await session.execute(text("SELECT last_insert_rowid()"))
            sess_id = result.scalar()
            await session.commit()

        async with get_session() as session:
            result = await get_cert_id_for_session(session, sess_id)
        assert result == cert_id

    async def test_returns_none_for_session_without_cert(self, db):
        """Sessions without certification_id return None."""
        async with get_session() as session:
            await session.execute(
                text("INSERT INTO study_sessions (user_id, session_type) VALUES (1, 'study')")
            )
            result = await session.execute(text("SELECT last_insert_rowid()"))
            sess_id = result.scalar()
            await session.commit()

        async with get_session() as session:
            result = await get_cert_id_for_session(session, sess_id)
        assert result is None

    async def test_returns_none_for_nonexistent_session(self, db):
        async with get_session() as session:
            result = await get_cert_id_for_session(session, 99999)
        assert result is None
