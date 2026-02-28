"""Shared helpers for exam/certification resolution."""

from __future__ import annotations

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


async def resolve_cert_id(session: AsyncSession, exam_code: str | None = None) -> int:
    """
    Resolve a certification ID from an optional exam_code.

    - exam_code given → look it up; raise ValueError if not found
    - exam_code=None + 1 cert in DB → auto-return it
    - exam_code=None + 0 certs → raise "run cert-pepper ingest first"
    - exam_code=None + multiple certs → raise with list of available codes
    """
    if exam_code is not None:
        result = await session.execute(
            text("SELECT id FROM certifications WHERE code = :code"),
            {"code": exam_code},
        )
        row = result.fetchone()
        if row is None:
            raise ValueError(
                f"Exam '{exam_code}' not found in database. Run cert-pepper ingest first."
            )
        return int(row[0])

    result = await session.execute(text("SELECT id, code FROM certifications"))
    rows = result.fetchall()

    if len(rows) == 0:
        raise ValueError("No exams found in database. Run cert-pepper ingest first.")

    if len(rows) == 1:
        return int(rows[0][0])

    codes = ", ".join(r[1] for r in rows)
    raise ValueError(
        f"Multiple exams found ({codes}). Specify exam_code parameter."
    )


async def get_cert_id_for_session(session: AsyncSession, session_db_id: int) -> int | None:
    """Return certification_id for a study session, or None if unset."""
    result = await session.execute(
        text("SELECT certification_id FROM study_sessions WHERE id = :sid"),
        {"sid": session_db_id},
    )
    row = result.fetchone()
    return row[0] if row else None
