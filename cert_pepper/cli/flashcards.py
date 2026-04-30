"""Interactive flashcard review session."""

from __future__ import annotations

import random

import click
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from sqlalchemy import text

from cert_pepper.db.connection import get_session
from cert_pepper.db.exams import resolve_cert_id

console = Console()

_QUIT_KEYS = {"q", "Q", "\x1b"}  # q, Q, Escape


def _getkey() -> str:
    """Read one keypress. Returns 'q' if user pressed q/Q/Escape."""
    ch = click.getchar(echo=False)
    return "q" if ch in _QUIT_KEYS else ""


async def run_flashcard_session(
    exam_code: str | None = None,
    domain: int | None = None,
    category: str | None = None,
    count: int | None = None,
    show_answer: bool = False,
) -> None:
    """Flip-style flashcard review — Enter reveals answer, Enter/Q advances."""
    async with get_session() as session:
        try:
            cert_id = await resolve_cert_id(session, exam_code)
        except ValueError as e:
            console.print(f"[red]{e}[/red]")
            return

        query = """
            SELECT f.id, f.front, f.back, f.tip, f.category,
                   d.number, d.name, a.full_term
            FROM flashcards f
            LEFT JOIN domains d ON d.id = f.domain_id
            LEFT JOIN acronyms a
                ON a.acronym = f.front AND a.certification_id = f.certification_id
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
        _card_id, front, back, _tip, cat, domain_num, _domain_name, full_term = card

        header_parts = [f"Flashcard {i}/{total}"]
        if domain_num is not None:
            header_parts.append(f"Domain {domain_num}")
        if cat:
            header_parts.append(cat)
        header = "  ·  ".join(header_parts)

        nav_hint = (
            "Enter to finish  ·  Q to quit"
            if i == total
            else "Enter to continue  ·  Q to quit"
        )

        if show_answer:
            # — combined panel: definition + term visible immediately —
            content = Text()
            content.append(back)
            content.append("\n\n")
            content.append("─" * 50)
            content.append("\n\n")
            content.append(front, style="bold")
            if full_term:
                content.append(f"\n{full_term}", style="dim")
            content.append(f"\n\n{nav_hint}", style="dim")

            console.clear()
            console.print(Panel(content, title=header, border_style="cyan"))

            if _getkey() == "q":
                shown = i
                break
        else:
            # — question side (definition) —
            question_content = Text()
            question_content.append(back)
            question_content.append("\n\n")
            question_content.append("Enter to reveal  ·  Q to quit", style="dim")

            console.clear()
            console.print(Panel(question_content, title=header, border_style="cyan"))

            if _getkey() == "q":
                shown = i - 1
                break

            # — answer side (term) —
            full_content = Text()
            full_content.append(back)
            full_content.append("\n\n")
            full_content.append("─" * 50)
            full_content.append("\n\n")
            full_content.append(front, style="bold")
            if full_term:
                full_content.append(f"\n{full_term}", style="dim")
            full_content.append(f"\n\n{nav_hint}", style="dim")

            console.clear()
            console.print(Panel(full_content, title=header, border_style="cyan"))

            if _getkey() == "q":
                shown = i
                break

        shown = i

    console.print(f"\n[green]✓ Done. Reviewed {shown}/{total} cards.[/green]")
