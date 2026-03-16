"""Batch pre-generation of AI explanations."""

from __future__ import annotations

from rich.console import Console
from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn
from rich.table import Table
from sqlalchemy import text

from cert_pepper.db.connection import get_session
from cert_pepper.models.content import Question

console = Console()


async def run_pregenerate(domain_filter: int | None = None) -> None:
    """Pre-generate AI explanations for all questions."""

    console.print("[cyan]Pre-generating AI explanations...[/cyan]")
    console.print("[dim]This runs once and stores results in the DB.[/dim]\n")

    async with get_session() as session:
        # Fetch questions
        params: dict[str, int] = {}
        domain_clause = ""
        if domain_filter:
            domain_clause = "AND d.number = :domain_filter"
            params["domain_filter"] = domain_filter
        result = await session.execute(
            text(f"""
                SELECT q.id, q.domain_id, d.number, q.number, q.stem,
                       q.option_a, q.option_b, q.option_c, q.option_d,
                       q.correct_answer, q.explanation, q.difficulty, q.source_file
                FROM questions q
                JOIN domains d ON d.id = q.domain_id
                WHERE 1=1 {domain_clause}
                ORDER BY d.number, q.number
            """),
            params,
        )
        rows = result.fetchall()
        questions = [
            Question(
                id=row[0], domain_id=row[1], domain_number=row[2], number=row[3],
                stem=row[4], option_a=row[5], option_b=row[6], option_c=row[7],
                option_d=row[8], correct_answer=row[9], explanation=row[10],
                difficulty=row[11], source_file=row[12],
            )
            for row in rows
        ]

        if not questions:
            console.print("[yellow]No questions found. Run `cert-pepper ingest` first.[/yellow]")
            return

        console.print(
            f"Found [cyan]{len(questions)}[/cyan] questions. "
            f"Generating explanations for wrong answers"
            f" (~{len(questions) * 3} API calls)...\n"
        )

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("{task.completed}/{task.total}"),
            console=console,
        ) as progress:
            task = progress.add_task("Generating...", total=len(questions))

            for q in questions:
                progress.update(task, description=f"Q{q.number} (D{q.domain_number})")
                # Generate for each wrong answer
                wrong_answers = [a for a in ["A", "B", "C", "D"] if a != q.correct_answer]
                for wrong in wrong_answers:
                    # Check cache
                    cached = await session.execute(
                        text("""
                            SELECT 1 FROM ai_explanations
                            WHERE content_type='question' AND content_id=:qid
                            AND explanation_type='full' AND selected_answer=:ans
                        """),
                        {"qid": q.id, "ans": wrong},
                    )
                    if cached.fetchone():
                        continue

                    try:
                        from cert_pepper.ai.explainer import get_explanation
                        await get_explanation(session, q, wrong)
                    except Exception as e:
                        console.print(f"\n[red]Error on Q{q.id}/{wrong}: {e}[/red]")

                progress.advance(task)

        # Show cache stats
        result = await session.execute(
            text(
                "SELECT COUNT(*), SUM(tokens_used), SUM(cached)"
                " FROM ai_explanations WHERE content_type='question'"
            )
        )
        stats = result.fetchone()
        assert stats is not None
        total_expl = stats[0] or 0
        total_tokens = stats[1] or 0
        cache_hits = stats[2] or 0

    table = Table(title="Pre-generation Complete", show_header=False)
    table.add_column("Metric", style="cyan")
    table.add_column("Value", justify="right")
    table.add_row("Explanations stored", str(total_expl))
    table.add_row("Total tokens used", f"{total_tokens:,}")
    table.add_row("Anthropic cache hits", str(cache_hits))
    table.add_row("Estimated cost", f"~${total_tokens / 1_000_000 * 3:.4f}")
    console.print(table)
    console.print(
        "\n[green]✓ All explanations pre-generated. Future sessions won't call the API.[/green]"
    )
