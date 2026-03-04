"""MCP Server 2: content — question bank, explanations, flashcards.

The get_explanation tool uses MCP sampling (ctx.session.create_message) to
delegate AI calls to the MCP client — no ANTHROPIC_API_KEY required.
"""

from __future__ import annotations

import json
from typing import Any

import httpx
from mcp.server.fastmcp import Context, FastMCP
from mcp.types import SamplingMessage, TextContent
from sqlalchemy.ext.asyncio import AsyncSession

from cert_pepper.db.connection import get_session, init_db
from cert_pepper.models.content import Question

mcp = FastMCP("cert-pepper-content")


async def _load_question(db: AsyncSession, question_id: int) -> Question | None:
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
async def get_explanation(
    question_id: int, selected_answer: str, ctx: Context[Any, Any, Any]
) -> str:
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
            explanation = (
                content_block.text if hasattr(content_block, "text") else str(content_block)
            )
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
    exam_code: str | None = None,
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

    if exam_code:
        clauses.append("c.code = :exam_code")
        params["exam_code"] = exam_code

    where = " AND ".join(clauses)
    join_cert = "JOIN certifications c ON c.id = d.certification_id" if exam_code else ""

    async with get_session() as db:
        result = await db.execute(
            text(f"""
                SELECT q.id, d.number, q.number, q.stem, q.correct_answer, q.difficulty
                FROM questions q JOIN domains d ON d.id = q.domain_id
                {join_cert}
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

    return json.dumps(
        {"id": row[0], "category": row[1], "front": row[2], "back": row[3], "tip": row[4]}
    )


@mcp.tool()
async def lookup_acronym(acronym: str, exam_code: str | None = None) -> str:
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


_BATCHES_PER_DOMAIN = 3
_QUESTIONS_PER_BATCH = 30

_EXAM_CONFIG_SYSTEM = """\
You are a certification exam expert. Return ONLY valid JSON with no markdown fencing, \
no extra commentary — just the raw JSON object.\
"""

_EXAM_CONFIG_USER = """\
Return a JSON object for the certification exam: "{exam_name}"

Required fields:
  code          — short exam code (e.g. "SY0-701", "CISSP")
  name          — full official exam name
  vendor        — issuing organisation (e.g. "CompTIA", "ISC2", "AWS")
  passing_score — integer passing score (e.g. 750)
  max_score     — integer maximum score (e.g. 900)
  domains       — array of objects, each with:
                    number     (int, starting at 1)
                    name       (string)
                    weight_pct (float, weights must sum to exactly 100.0)

Return nothing but the JSON object.\
"""

_QUESTIONS_SYSTEM = """\
You are a certification exam question writer. Generate EXACTLY {n} questions in \
this markdown format (copy the structure precisely):

**Q{{number}}.** Question stem here?

A) Option A
B) Option B
C) Option C
D) Option D

<details><summary>Answer</summary>

**X) Correct option text**

Explanation of why X is correct and why the distractors are wrong.

</details>

---

Rules:
- Exactly 4 options labelled A) through D).
- Exactly 1 correct answer per question.
- A `---` separator between questions but NOT after the last one.
- Number questions consecutively starting at the number given in the prompt.
- Questions must test application/analysis (exam-difficulty), not just recall.
- Never expand acronyms in answer options. Use the acronym alone (e.g. "SOAR" not \
"SOAR — Security Orchestration, Automation, and Response"). Knowing acronym meanings \
is a core exam skill.\
"""

_QUESTIONS_USER = """\
Generate {n} practice questions (Q{start} through Q{end}) for:
  Exam:   {exam_name}
  Domain {domain_number}: {domain_name} ({weight_pct}% of exam)
{research_context}
Focus on realistic exam-difficulty scenarios covering the full breadth of this domain.\
"""

_VENDOR_SUBREDDITS: dict[str, str] = {
    "comptia": "CompTIA",
    "isc2": "cissp",
    "aws": "AWSCertifications",
    "amazon": "AWSCertifications",
    "microsoft": "AzureCertifications",
    "azure": "AzureCertifications",
    "google": "googlecloud",
    "gcp": "googlecloud",
}

_REDDIT_SEARCH_URL = "https://www.reddit.com/search.json"
_REDDIT_SUBREDDIT_URL = "https://www.reddit.com/r/{sub}/search.json"
_REDDIT_HEADERS = {"User-Agent": "cert-pepper/1.0 (exam study tool; educational use)"}

_RESEARCH_SYNTHESIS_SYSTEM = """\
You are a certification exam intelligence analyst. Read community discussion \
posts and extract concise, actionable insights about the real exam. \
Return ONLY a bulleted list (≤15 bullets, each starting with "- "). \
No preamble, no commentary, no headings.\
"""

_RESEARCH_SYNTHESIS_USER = """\
Below are excerpts from Reddit discussions about the {exam_name} exam. \
Synthesize into ≤15 bullet points a question writer should know: \
tricky topics, common traps, frequently tested concepts, areas of confusion.

--- EXCERPTS START ---
{excerpts_text}
--- EXCERPTS END ---

Return only the bullet list.\
"""


def _strip_json_fences(text: str) -> str:
    """Remove optional ```json … ``` fences an LLM may wrap around JSON."""
    text = text.strip()
    if text.startswith("```"):
        lines = text.splitlines()
        # drop first line (```json or ```) and last line (```)
        text = "\n".join(lines[1:-1]).strip()
    return text


async def _fetch_reddit_excerpts(exam_name: str, vendor: str) -> list[str]:
    """Fetch top Reddit post excerpts about the exam. Returns [] on any failure."""
    subreddit = _VENDOR_SUBREDDITS.get(vendor.lower())

    urls: list[str] = [_REDDIT_SEARCH_URL]
    if subreddit:
        urls.append(_REDDIT_SUBREDDIT_URL.format(sub=subreddit))

    seen_titles: set[str] = set()
    excerpts: list[str] = []

    try:
        async with httpx.AsyncClient(headers=_REDDIT_HEADERS, timeout=10.0) as client:
            for url in urls:
                try:
                    params = {"q": exam_name, "sort": "top", "t": "year", "limit": "20"}
                    resp = await client.get(url, params=params)
                    resp.raise_for_status()
                    data = resp.json()
                    children = data["data"]["children"]
                    for child in children:
                        post = child["data"]
                        title = post.get("title", "")
                        selftext = post.get("selftext", "")
                        score = post.get("score", 0)
                        if score < 5:
                            continue
                        if selftext in ("[removed]", "[deleted]", ""):
                            continue
                        if title in seen_titles:
                            continue
                        seen_titles.add(title)
                        excerpts.append(f"{title}: {selftext[:400]}")
                except Exception:
                    continue
    except Exception:
        return []

    return excerpts


async def _build_research_context(
    exam_name: str, vendor: str, ctx: Context[Any, Any, Any]
) -> str:
    """Synthesize Reddit research into exam insights via MCP sampling.

    Returns formatted string for injection into _QUESTIONS_USER, or '' on failure.
    """
    try:
        excerpts = await _fetch_reddit_excerpts(exam_name, vendor)
        if not excerpts:
            return ""

        excerpts_text = "\n\n".join(excerpts)
        result = await ctx.session.create_message(
            messages=[
                SamplingMessage(
                    role="user",
                    content=TextContent(
                        type="text",
                        text=_RESEARCH_SYNTHESIS_USER.format(
                            exam_name=exam_name, excerpts_text=excerpts_text
                        ),
                    ),
                )
            ],
            system_prompt=_RESEARCH_SYNTHESIS_SYSTEM,
            max_tokens=512,
        )
        bullets = result.content.text if hasattr(result.content, "text") else str(result.content)
        header = (
            "\nCommunity exam insights"
            " (incorporate these into question difficulty and distractors):\n"
        )
        return header + bullets.strip() + "\n"
    except Exception:
        return ""


@mcp.tool()
async def setup_exam(exam_name: str, ctx: Context[Any, Any, Any]) -> str:
    """Prepare a full question bank for an exam.

    Checks if the exam already exists in the DB. If it does, returns a
    ready status with question count. If not, uses MCP sampling to:
    1. Generate the exam structure (code, name, vendor, domains + weights)
    2. Generate ~90 practice questions per domain in batches of 30
    3. Insert everything into the DB

    exam_name: Natural language exam name, e.g. "CompTIA Security+ SY0-701",
               "CISSP", "AWS Solutions Architect Associate"
    """
    from sqlalchemy import text as sql_text

    from cert_pepper.ingestion.loader import ingest_exam_config, ingest_questions
    from cert_pepper.ingestion.questions import parse_questions_text
    from cert_pepper.models.content import ExamConfig, ExamDomain

    q = f"%{exam_name}%"

    async with get_session() as db:
        # ── Check for existing exam ──────────────────────────────────────────
        result = await db.execute(
            sql_text(
                "SELECT id, code, name FROM certifications "
                "WHERE LOWER(code) LIKE LOWER(:q) OR LOWER(name) LIKE LOWER(:q)"
            ),
            {"q": q},
        )
        row = result.fetchone()

        if row:
            cert_id, exam_code, exam_full_name = row[0], row[1], row[2]
            count_result = await db.execute(
                sql_text(
                    "SELECT COUNT(*) FROM questions qst "
                    "JOIN domains d ON qst.domain_id = d.id "
                    "WHERE d.certification_id = :cert_id"
                ),
                {"cert_id": cert_id},
            )
            question_count = count_result.scalar() or 0
            return json.dumps({
                "status": "ready",
                "exam_code": exam_code,
                "exam_name": exam_full_name,
                "question_count": question_count,
            })

    # ── Exam not found — generate via MCP sampling ───────────────────────────

    # Step 1: generate exam config
    config_result = await ctx.session.create_message(
        messages=[
            SamplingMessage(
                role="user",
                content=TextContent(
                    type="text",
                    text=_EXAM_CONFIG_USER.format(exam_name=exam_name),
                ),
            )
        ],
        system_prompt=_EXAM_CONFIG_SYSTEM,
        max_tokens=1024,
    )
    raw_json = _strip_json_fences(
        config_result.content.text
        if hasattr(config_result.content, "text")
        else str(config_result.content)
    )

    try:
        config_data = json.loads(raw_json)
    except json.JSONDecodeError as exc:
        return json.dumps({"error": f"Failed to parse exam config JSON: {exc}", "raw": raw_json})

    try:
        exam_config = ExamConfig(
            code=config_data["code"],
            name=config_data["name"],
            vendor=config_data.get("vendor", ""),
            passing_score=int(config_data.get("passing_score", 750)),
            max_score=int(config_data.get("max_score", 900)),
            domains=[
                ExamDomain(
                    number=int(d["number"]),
                    name=d["name"],
                    weight_pct=float(d["weight_pct"]),
                )
                for d in config_data.get("domains", [])
            ],
        )
    except (KeyError, TypeError, ValueError) as exc:
        return json.dumps({"error": f"Invalid exam config structure: {exc}", "raw": raw_json})

    # Step 2: insert config, then generate questions domain by domain
    research_context = await _build_research_context(exam_config.name, exam_config.vendor, ctx)

    total_inserted = 0
    async with get_session() as db:
        cert_id = await ingest_exam_config(db, exam_config)

        for domain in exam_config.domains:
            for batch_idx in range(_BATCHES_PER_DOMAIN):
                start = batch_idx * _QUESTIONS_PER_BATCH + 1
                end = start + _QUESTIONS_PER_BATCH - 1

                q_result = await ctx.session.create_message(
                    messages=[
                        SamplingMessage(
                            role="user",
                            content=TextContent(
                                type="text",
                                text=_QUESTIONS_USER.format(
                                    n=_QUESTIONS_PER_BATCH,
                                    start=start,
                                    end=end,
                                    exam_name=exam_config.name,
                                    domain_number=domain.number,
                                    domain_name=domain.name,
                                    weight_pct=domain.weight_pct,
                                    research_context=research_context,
                                ),
                            ),
                        )
                    ],
                    system_prompt=_QUESTIONS_SYSTEM.format(n=_QUESTIONS_PER_BATCH),
                    max_tokens=8192,
                )
                raw_text = (
                    q_result.content.text
                    if hasattr(q_result.content, "text")
                    else str(q_result.content)
                )
                parsed = parse_questions_text(raw_text, domain_number=domain.number)
                inserted = await ingest_questions(db, parsed, cert_id=cert_id)
                total_inserted += inserted

    return json.dumps({
        "status": "created",
        "exam_code": exam_config.code,
        "exam_name": exam_config.name,
        "question_count": total_inserted,
        "domains": [
            {"number": d.number, "name": d.name, "weight_pct": d.weight_pct}
            for d in exam_config.domains
        ],
    })


def serve() -> None:
    """Entry point for the content MCP server (stdio transport)."""
    import asyncio

    asyncio.run(init_db())
    mcp.run(transport="stdio")


if __name__ == "__main__":
    serve()
