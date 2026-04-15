# Flashcard Command Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a `cert-pepper flashcard` command that displays flashcards one at a time, showing front and answer together in a single panel with shuffle and optional filters.

**Architecture:** One new file `cert_pepper/cli/flashcards.py` contains `run_flashcard_session()`. It fetches all matching flashcards in a single DB query, shuffles them, then renders each as a Rich Panel with front, answer, and optional tip. `main.py` registers the `flashcard` Typer command. No DB writes — the session is read-only.

**Tech Stack:** Python, Rich (Panel, Text, Prompt), SQLAlchemy async text() queries, pytest with asyncio_mode=auto, unittest.mock.patch

---

## File Map

| File | Change |
|------|--------|
| `tests/conftest.py` | Add `seed_flashcard()` helper after `seed_session()` (line 177) |
| `tests/test_flashcards.py` | Create — 5 tests in `TestFlashcardSession` |
| `cert_pepper/cli/flashcards.py` | Create — `run_flashcard_session()` async function |
| `cert_pepper/cli/main.py` | Add `@app.command("flashcard")` before `@app.command("pregenerate")` (line 243) |

---

### Task 1: seed_flashcard() helper + failing tests

**Files:**
- Modify: `tests/conftest.py:177`
- Create: `tests/test_flashcards.py`

- [ ] **Step 1: Add `seed_flashcard()` to conftest.py after `seed_session()` (after line 177)**

```python
async def seed_flashcard(
    session,
    front: str = "Term",
    back: str = "Definition",
    tip: str = "",
    category: str = "General",
    domain_number: int = 1,
    cert_id: int | None = None,
) -> int:
    """Insert a flashcard and return its id."""
    if cert_id is not None:
        result = await session.execute(
            text("SELECT id FROM domains WHERE number = :n AND certification_id = :c"),
            {"n": domain_number, "c": cert_id},
        )
    else:
        result = await session.execute(
            text("SELECT id FROM domains WHERE number = :n"),
            {"n": domain_number},
        )
    domain_id = result.scalar()
    assert domain_id is not None, f"Domain {domain_number} not found — was init_db called?"
    await session.execute(
        text("""
            INSERT INTO flashcards (domain_id, category, front, back, tip, certification_id)
            VALUES (:did, :cat, :front, :back, :tip, :cid)
        """),
        {"did": domain_id, "cat": category, "front": front,
         "back": back, "tip": tip, "cid": cert_id},
    )
    result = await session.execute(text("SELECT last_insert_rowid()"))
    return result.scalar()
```

- [ ] **Step 2: Create `tests/test_flashcards.py` with all 5 failing tests**

```python
"""Tests for the flashcard review session."""

from __future__ import annotations

from unittest.mock import patch

import pytest

from tests.conftest import (
    seed_certification,
    seed_domains_for_cert,
    seed_flashcard,
)


class TestFlashcardSession:
    async def test_run_flashcard_session_shows_all_cards(self, db):
        """Three cards → three panel prints plus one completion print."""
        from cert_pepper.cli.flashcards import run_flashcard_session

        cert_id = await seed_certification(db, code="FC01")
        await seed_domains_for_cert(db, cert_id)
        await seed_flashcard(db, front="Term 1", back="Def 1", cert_id=cert_id)
        await seed_flashcard(db, front="Term 2", back="Def 2", cert_id=cert_id)
        await seed_flashcard(db, front="Term 3", back="Def 3", cert_id=cert_id)

        printed = []
        with patch("cert_pepper.cli.flashcards.Prompt.ask", return_value=""):
            with patch("cert_pepper.cli.flashcards.console.print",
                       side_effect=printed.append):
                await run_flashcard_session(exam_code="FC01")

        # 3 panel prints + 1 completion message
        assert len(printed) == 4

    async def test_run_flashcard_session_domain_filter(self, db):
        """Only cards from the requested domain are shown."""
        from cert_pepper.cli.flashcards import run_flashcard_session

        cert_id = await seed_certification(db, code="FC02")
        await seed_domains_for_cert(db, cert_id, [(1, "D1", 50.0), (2, "D2", 50.0)])
        await seed_flashcard(db, front="D1 Term", back="D1 Def",
                             domain_number=1, cert_id=cert_id)
        await seed_flashcard(db, front="D2 Term", back="D2 Def",
                             domain_number=2, cert_id=cert_id)

        printed = []
        with patch("cert_pepper.cli.flashcards.Prompt.ask", return_value=""):
            with patch("cert_pepper.cli.flashcards.console.print",
                       side_effect=printed.append):
                await run_flashcard_session(exam_code="FC02", domain=1)

        # 1 panel + 1 completion
        assert len(printed) == 2

    async def test_run_flashcard_session_category_filter(self, db):
        """Only cards from the requested category are shown."""
        from cert_pepper.cli.flashcards import run_flashcard_session

        cert_id = await seed_certification(db, code="FC03")
        await seed_domains_for_cert(db, cert_id)
        await seed_flashcard(db, front="Cat A Term", back="Cat A Def",
                             category="Alpha", cert_id=cert_id)
        await seed_flashcard(db, front="Cat B Term", back="Cat B Def",
                             category="Beta", cert_id=cert_id)

        printed = []
        with patch("cert_pepper.cli.flashcards.Prompt.ask", return_value=""):
            with patch("cert_pepper.cli.flashcards.console.print",
                       side_effect=printed.append):
                await run_flashcard_session(exam_code="FC03", category="Alpha")

        # 1 panel + 1 completion
        assert len(printed) == 2

    async def test_run_flashcard_session_count_cap(self, db):
        """count=2 with 5 cards shows only 2 panels."""
        from cert_pepper.cli.flashcards import run_flashcard_session

        cert_id = await seed_certification(db, code="FC04")
        await seed_domains_for_cert(db, cert_id)
        for i in range(5):
            await seed_flashcard(db, front=f"Term {i}", back=f"Def {i}",
                                 cert_id=cert_id)

        printed = []
        with patch("cert_pepper.cli.flashcards.Prompt.ask", return_value=""):
            with patch("cert_pepper.cli.flashcards.console.print",
                       side_effect=printed.append):
                await run_flashcard_session(exam_code="FC04", count=2)

        # 2 panels + 1 completion
        assert len(printed) == 3

    async def test_run_flashcard_session_no_cards_exits_cleanly(self, db):
        """No flashcards for the cert → single yellow warning, no crash."""
        from cert_pepper.cli.flashcards import run_flashcard_session

        cert_id = await seed_certification(db, code="FC05")
        await seed_domains_for_cert(db, cert_id)
        # no flashcards seeded

        printed = []
        with patch("cert_pepper.cli.flashcards.console.print",
                   side_effect=printed.append):
            await run_flashcard_session(exam_code="FC05")

        assert len(printed) == 1
        assert "No flashcards" in str(printed[0])
```

- [ ] **Step 3: Run tests to confirm they fail**

```bash
uv run pytest tests/test_flashcards.py -v
```

Expected: 5 errors — `ModuleNotFoundError: No module named 'cert_pepper.cli.flashcards'`

- [ ] **Step 4: Commit the failing tests + seed helper**

```bash
git add tests/conftest.py tests/test_flashcards.py
git commit -m "test: add failing tests and seed_flashcard for flashcard command"
```

---

### Task 2: Implement cert_pepper/cli/flashcards.py

**Files:**
- Create: `cert_pepper/cli/flashcards.py`

- [ ] **Step 1: Create `cert_pepper/cli/flashcards.py`**

```python
"""Interactive flashcard review session."""

from __future__ import annotations

import random

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.text import Text
from sqlalchemy import text

from cert_pepper.db.connection import get_session
from cert_pepper.db.exams import resolve_cert_id

console = Console()


async def run_flashcard_session(
    exam_code: str | None = None,
    domain: int | None = None,
    category: str | None = None,
    count: int | None = None,
) -> None:
    """Display flashcards one at a time — front and answer visible together."""
    async with get_session() as session:
        try:
            cert_id = await resolve_cert_id(session, exam_code)
        except ValueError as e:
            console.print(f"[red]{e}[/red]")
            return

        query = """
            SELECT f.id, f.front, f.back, f.tip, f.category,
                   d.number, d.name
            FROM flashcards f
            LEFT JOIN domains d ON d.id = f.domain_id
            WHERE f.certification_id = :cert_id
        """
        params: dict = {"cert_id": cert_id}

        if domain is not None:
            query += " AND d.number = :domain"
            params["domain"] = domain

        if category is not None:
            query += " AND f.category = :category"
            params["category"] = category

        result = await session.execute(text(query), params)
        rows = result.fetchall()

    if not rows:
        console.print("[yellow]No flashcards found for the given filters.[/yellow]")
        return

    cards = list(rows)
    random.shuffle(cards)
    if count is not None:
        cards = cards[:count]

    total = len(cards)
    shown = 0

    for i, card in enumerate(cards, 1):
        _card_id, front, back, tip, cat, domain_num, _domain_name = card

        content = Text()
        content.append(front, style="bold")
        content.append("\n\n")
        content.append("─" * 50)
        content.append("\n\n")
        content.append(back)
        if tip:
            content.append(f"\n\n💡 {tip}")

        header_parts = [f"Flashcard {i}/{total}"]
        if domain_num is not None:
            header_parts.append(f"Domain {domain_num}")
        if cat:
            header_parts.append(cat)
        header = "  ·  ".join(header_parts)

        console.print(Panel(content, title=header, border_style="cyan"))
        shown = i

        if i < total:
            response = Prompt.ask("[Enter] Next  [Q] Quit", default="")
            if response.strip().lower() == "q":
                break

    console.print(f"\n[green]✓ Done. Reviewed {shown}/{total} cards.[/green]")
```

- [ ] **Step 2: Run the tests to confirm they pass**

```bash
uv run pytest tests/test_flashcards.py -v
```

Expected: 5 passed

- [ ] **Step 3: Run the full suite to confirm no regressions**

```bash
uv run pytest -q
```

Expected: all tests pass (378+ passing, 0 failures)

- [ ] **Step 4: Commit**

```bash
git add cert_pepper/cli/flashcards.py
git commit -m "feat: implement run_flashcard_session"
```

---

### Task 3: Wire the CLI command in main.py

**Files:**
- Modify: `cert_pepper/cli/main.py:243`

- [ ] **Step 1: Add the `flashcard` command to `main.py` before the `pregenerate` command (before line 243)**

```python
@app.command("flashcard")
def flashcard(
    exam: str | None = typer.Option(
        None, "--exam", "-e",
        help="Exam code (e.g. CY0-001). Auto-detects when only one exam is present."
    ),
    domain: int | None = typer.Option(
        None, "--domain", "-d", help="Filter to domain number."
    ),
    category: str | None = typer.Option(
        None, "--category", "-c", help="Filter to category name (e.g. 'AI Attacks')."
    ),
    count: int | None = typer.Option(
        None, "--count", "-n", help="Max number of cards to show."
    ),
) -> None:
    """Review flashcards — front and answer shown together."""
    import asyncio

    from cert_pepper.cli.flashcards import run_flashcard_session

    asyncio.run(
        run_flashcard_session(
            exam_code=exam, domain=domain, category=category, count=count
        )
    )
```

- [ ] **Step 2: Verify the command appears in help**

```bash
uv run cert-pepper --help
```

Expected: `flashcard` listed under Commands

- [ ] **Step 3: Run the full test suite**

```bash
uv run pytest -q
```

Expected: all tests pass

- [ ] **Step 4: Commit**

```bash
git add cert_pepper/cli/main.py
git commit -m "feat: add flashcard CLI command"
```
