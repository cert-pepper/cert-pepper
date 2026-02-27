"""MCP Server 2: content — question bank, explanations, flashcards.

The get_explanation tool uses MCP sampling (ctx.session.create_message) to
delegate AI calls to the MCP client — no ANTHROPIC_API_KEY required.
"""

from __future__ import annotations

import json
from typing import Any

from mcp.server.fastmcp import Context, FastMCP
from mcp.types import SamplingMessage, TextContent

from cert_pepper.db.connection import get_session, init_db
from cert_pepper.models.content import Question

mcp = FastMCP("cert-pepper-content")


async def _load_question(db, question_id: int) -> Question | None:
    from sqlalchemy import text

    result = await db.execute(
        text("""
            SELECT q.id, q.domain_id, d.number, q.number, q.stem,
                   q.option_a, q.option_b, q.option_c, q.option_d,
                   q.correct_answer, q.explanation, q.difficulty, q.source_file
            FROM questions q JOIN domains d ON d.id = q.domain_id
            WHERE q.id = :qid
        """),
        {"qid": question_id},
    )
    row = result.fetchone()
    if not row:
        return None
    return Question(
        id=row[0],
        domain_id=row[1],
        domain_number=row[2],
        number=row[3],
        stem=row[4],
        option_a=row[5],
        option_b=row[6],
        option_c=row[7],
        option_d=row[8],
        correct_answer=row[9],
        explanation=row[10],
        difficulty=row[11],
        source_file=row[12],
    )


@mcp.tool()
async def get_explanation(question_id: int, selected_answer: str, ctx: Context) -> str:
    """Get an AI explanation for a question answer.

    Checks DB cache first. On cache miss, uses MCP sampling to generate the
    explanation via the connected MCP client — no ANTHROPIC_API_KEY needed.
    """
    from cert_pepper.ai.explainer import _build_user_message, _get_cached, _store_explanation
    from cert_pepper.ai.prompts import get_explainer_system

    selected = selected_answer.upper()

    async with get_session() as db:
        q = await _load_question(db, question_id)
        if q is None:
            return json.dumps({"error": "Question not found"})

        # Correct answer: return stored markdown explanation directly
        if selected == q.correct_answer and q.explanation:
            return json.dumps({
                "question_id": question_id,
                "selected_answer": selected,
                "correct_answer": q.correct_answer,
                "is_correct": True,
                "explanation": q.explanation,
                "source": "stored",
            })

        # Check DB cache
        cached = await _get_cached(db, q.id, "full", selected)
        if cached:
            return json.dumps({
                "question_id": question_id,
                "selected_answer": selected,
                "correct_answer": q.correct_answer,
                "is_correct": selected == q.correct_answer,
                "explanation": cached,
                "source": "cache",
            })

        # Generate via MCP sampling
        system_prompt = get_explainer_system(q.domain_number)
        user_msg = _build_user_message(q, selected)
        explanation = ""
        source = "error"

        try:
            result = await ctx.session.create_message(
                messages=[
                    SamplingMessage(
                        role="user",
                        content=TextContent(type="text", text=user_msg),
                    )
                ],
                system_prompt=system_prompt,
                max_tokens=512,
            )
            content_block = result.content
            explanation = content_block.text if hasattr(content_block, "text") else str(content_block)
            source = "mcp-sampling"

            # Store in DB cache
            await _store_explanation(
                db,
                question_id=q.id,
                explanation_type="full",
                selected_answer=selected,
                model="mcp-sampling",
                prompt_hash="",
                content=explanation,
                tokens=0,
                cached=False,
            )
        except Exception as exc:
            # Fallback: return the markdown explanation if available
            if q.explanation:
                explanation = q.explanation
                source = "stored-fallback"
            else:
                explanation = f"Could not generate explanation: {exc}"

    return json.dumps({
        "question_id": question_id,
        "selected_answer": selected,
        "correct_answer": q.correct_answer,
        "is_correct": selected == q.correct_answer,
        "explanation": explanation,
        "source": source,
    })


@mcp.tool()
async def get_question(question_id: int) -> str:
    """Get full question details by ID."""
    from sqlalchemy import text

    async with get_session() as db:
        result = await db.execute(
            text("""
                SELECT q.id, q.domain_id, d.number, q.number, q.stem,
                       q.option_a, q.option_b, q.option_c, q.option_d,
                       q.correct_answer, q.explanation
                FROM questions q JOIN domains d ON d.id = q.domain_id
                WHERE q.id = :qid
            """),
            {"qid": question_id},
        )
        row = result.fetchone()
        if not row:
            return json.dumps({"error": "Question not found"})

    return json.dumps({
        "id": row[0],
        "domain": row[2],
        "number": row[3],
        "stem": row[4],
        "options": {"A": row[5], "B": row[6], "C": row[7], "D": row[8]},
        "correct_answer": row[9],
        "explanation": row[10],
    })


@mcp.tool()
async def search_questions(
    domain: int | None = None,
    difficulty_max: float = 1.0,
    keyword: str = "",
    limit: int = 10,
) -> str:
    """Search questions by domain, difficulty, or keyword."""
    from sqlalchemy import text

    clauses = ["q.difficulty <= :diff_max"]
    params: dict[str, Any] = {"diff_max": difficulty_max, "limit": limit}

    if domain:
        clauses.append("d.number = :domain")
        params["domain"] = domain

    if keyword:
        clauses.append("(q.stem LIKE :kw OR q.explanation LIKE :kw)")
        params["kw"] = f"%{keyword}%"

    where = " AND ".join(clauses)

    async with get_session() as db:
        result = await db.execute(
            text(f"""
                SELECT q.id, d.number, q.number, q.stem, q.correct_answer, q.difficulty
                FROM questions q JOIN domains d ON d.id = q.domain_id
                WHERE {where}
                ORDER BY q.difficulty ASC
                LIMIT :limit
            """),
            params,
        )
        rows = result.fetchall()

    questions = [
        {
            "id": row[0],
            "domain": row[1],
            "number": row[2],
            "stem": row[3][:120] + "..." if len(row[3]) > 120 else row[3],
            "correct_answer": row[4],
            "difficulty": round(row[5], 2),
        }
        for row in rows
    ]
    return json.dumps({"count": len(questions), "questions": questions})


@mcp.tool()
async def get_flashcard(flashcard_id: int) -> str:
    """Get a flashcard by ID."""
    from sqlalchemy import text

    async with get_session() as db:
        result = await db.execute(
            text("SELECT id, category, front, back, tip FROM flashcards WHERE id=:fid"),
            {"fid": flashcard_id},
        )
        row = result.fetchone()
        if not row:
            return json.dumps({"error": "Flashcard not found"})

    return json.dumps({"id": row[0], "category": row[1], "front": row[2], "back": row[3], "tip": row[4]})


@mcp.tool()
async def lookup_acronym(acronym: str) -> str:
    """Look up an acronym's full meaning."""
    from sqlalchemy import text

    acr = acronym.upper().strip()
    async with get_session() as db:
        result = await db.execute(
            text("SELECT acronym, full_term, category FROM acronyms WHERE UPPER(acronym)=:acr"),
            {"acr": acr},
        )
        row = result.fetchone()

    if not row:
        return json.dumps({"error": f"Acronym '{acr}' not found in database."})

    return json.dumps({"acronym": row[0], "full_term": row[1], "category": row[2]})


@mcp.resource("content://questions/all")
async def all_questions() -> str:
    """All questions in the database."""
    from sqlalchemy import text

    async with get_session() as db:
        result = await db.execute(
            text("""
                SELECT q.id, d.number, q.stem, q.option_a, q.option_b,
                       q.option_c, q.option_d, q.correct_answer
                FROM questions q JOIN domains d ON d.id = q.domain_id
                ORDER BY d.number, q.number
            """)
        )
        rows = result.fetchall()
    data = [
        {
            "id": r[0],
            "domain": r[1],
            "stem": r[2],
            "options": {"A": r[3], "B": r[4], "C": r[5], "D": r[6]},
            "correct": r[7],
        }
        for r in rows
    ]
    return json.dumps(data)


@mcp.resource("content://acronyms")
async def acronym_list() -> str:
    """Full Security+ acronym reference."""
    from sqlalchemy import text

    async with get_session() as db:
        result = await db.execute(
            text("SELECT acronym, full_term, category FROM acronyms ORDER BY acronym")
        )
        rows = result.fetchall()
    data = [{"acronym": r[0], "full_term": r[1], "category": r[2]} for r in rows]
    return json.dumps(data)


def serve() -> None:
    """Entry point for the content MCP server (stdio transport)."""
    import asyncio

    asyncio.run(init_db())
    mcp.run(transport="stdio")


if __name__ == "__main__":
    serve()
