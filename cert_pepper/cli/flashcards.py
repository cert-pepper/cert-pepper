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
    i = 0

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

        if i < total:
            response = Prompt.ask("[Enter] Next  [Q] Quit", default="")
            if response.strip().lower() == "q":
                break

    console.print(f"\n[green]✓ Done. Reviewed {i}/{total} cards.[/green]")
