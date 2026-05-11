"""Shared helpers for exam/certification resolution."""

from __future__ import annotations

from dataclasses import dataclass, field

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


@dataclass(frozen=True)
class ExamChoice:
    """A selectable exam option for CLI or MCP flows."""

    id: int
    code: str
    name: str


@dataclass(frozen=True)
class ExamResolutionResult:
    """Structured result for exam resolution without using exceptions for choice prompts."""

    status: str
    cert_id: int | None = None
    options: list[ExamChoice] = field(default_factory=list)


async def list_exam_choices(session: AsyncSession) -> list[ExamChoice]:
    """Return all available exams sorted for stable display and testing."""
    result = await session.execute(
        text("SELECT id, code, name FROM certifications ORDER BY code")
    )
    return [
        ExamChoice(id=int(row[0]), code=str(row[1]), name=str(row[2]))
        for row in result.fetchall()
    ]


async def match_exam_choices(session: AsyncSession, query: str) -> list[ExamChoice]:
    """Return exams whose code or name contains the given query, case-insensitively."""
    q = f"%{query.strip()}%"
    result = await session.execute(
        text("""
            SELECT id, code, name
            FROM certifications
            WHERE LOWER(code) LIKE LOWER(:q) OR LOWER(name) LIKE LOWER(:q)
            ORDER BY code
        """),
        {"q": q},
    )
    return [
        ExamChoice(id=int(row[0]), code=str(row[1]), name=str(row[2]))
        for row in result.fetchall()
    ]


async def resolve_exam_selection(
    session: AsyncSession, exam_code: str | None = None
) -> ExamResolutionResult:
    """Resolve an exam or return a structured choice prompt for multi-exam flows."""
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
        return ExamResolutionResult(status="resolved", cert_id=int(row[0]))

    rows = await list_exam_choices(session)

    if len(rows) == 0:
        raise ValueError("No exams found in database. Run cert-pepper ingest first.")

    if len(rows) == 1:
        return ExamResolutionResult(status="resolved", cert_id=rows[0].id)

    return ExamResolutionResult(status="selection_required", options=rows)


async def resolve_cert_id(session: AsyncSession, exam_code: str | None = None) -> int:
    """
    Resolve a certification ID from an optional exam_code.

    - exam_code given → look it up; raise ValueError if not found
    - exam_code=None + 1 cert in DB → auto-return it
    - exam_code=None + 0 certs → raise "run cert-pepper ingest first"
    - exam_code=None + multiple certs → raise with list of available codes
    """
    selection = await resolve_exam_selection(session, exam_code)
    if selection.status == "resolved" and selection.cert_id is not None:
        return selection.cert_id

    codes = ", ".join(option.code for option in selection.options)
    raise ValueError(f"Multiple exams found ({codes}). Specify exam_code parameter.")


async def get_cert_id_for_session(session: AsyncSession, session_db_id: int) -> int | None:
    """Return certification_id for a study session, or None if unset."""
    result = await session.execute(
        text("SELECT certification_id FROM study_sessions WHERE id = :sid"),
        {"sid": session_db_id},
    )
    row = result.fetchone()
    return row[0] if row else None
