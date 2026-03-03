"""Main Typer application entry point."""


import typer

app = typer.Typer(
    name="cert-pepper",
    help="AI-powered adaptive certification prep that learns what you don't know.",
    rich_markup_mode="rich",
    no_args_is_help=True,
)

# Sub-command groups
db_app = typer.Typer(help="Database management commands.")
app.add_typer(db_app, name="db")


@db_app.command("init")
def db_init(
    reset: bool = typer.Option(False, "--reset", help="Drop and recreate the database."),
) -> None:
    """Initialize the database schema and seed default data."""
    import asyncio

    from rich.console import Console

    from cert_pepper.config import get_settings
    from cert_pepper.db.connection import init_db

    console = Console()
    settings = get_settings()

    if reset:
        db_path = settings.db_path
        if db_path.exists():
            db_path.unlink()
            console.print(f"[yellow]Removed existing database: {db_path}[/yellow]")

    console.print("[cyan]Initializing database...[/cyan]")
    asyncio.run(init_db())
    console.print(f"[green]✓ Database ready at {settings.db_path}[/green]")


@app.command("ingest")
def ingest(
    dry_run: bool = typer.Option(False, "--dry-run", help="Parse only, don't write to DB."),
    content_root: str | None = typer.Option(
        None, "--content-root", help="Path to security-plus repo root."
    ),
) -> None:
    """Parse markdown study content and load into database."""
    import asyncio

    from rich.console import Console
    from rich.table import Table

    from cert_pepper.config import Settings, get_settings
    from cert_pepper.db.connection import get_session
    from cert_pepper.ingestion.loader import run_ingestion

    console = Console()
    settings = get_settings()
    if content_root:
        from pathlib import Path
        settings = Settings(content_root=Path(content_root))

    console.print(f"[cyan]Ingesting content from: {settings.content_root}[/cyan]")
    if dry_run:
        console.print("[yellow]DRY RUN — nothing will be written to the database[/yellow]")

    async def _run() -> dict[str, int]:
        async with get_session() as session:
            return await run_ingestion(session, settings, dry_run=dry_run)

    counts = asyncio.run(_run())

    table = Table(title="Ingestion Results", show_header=True)
    table.add_column("Content Type", style="cyan")
    table.add_column("Count", justify="right", style="green")
    table.add_row("Questions", str(counts["questions"]))
    table.add_row("Flashcards", str(counts["flashcards"]))
    table.add_row("Acronyms", str(counts["acronyms"]))
    console.print(table)

    if dry_run:
        console.print("[yellow]Dry run complete. No data written.[/yellow]")
    else:
        console.print("[green]✓ Ingestion complete.[/green]")


@app.command("study")
def study(
    domain: int | None = typer.Option(
        None, "--domain", "-d", help="Domain number (1-5). Default: adaptive."
    ),
    count: int = typer.Option(25, "--count", "-n", help="Number of questions per session."),
    no_ai: bool = typer.Option(False, "--no-ai", help="Skip AI explanations (offline mode)."),
    exam: str | None = typer.Option(
        None, "--exam", "-e",
        help="Exam code (e.g. SY0-701). Auto-detects when only one exam is present."
    ),
) -> None:
    """Start an adaptive study session."""
    import asyncio

    from cert_pepper.cli.study import run_study_session
    asyncio.run(run_study_session(domain=domain, count=count, use_ai=not no_ai, exam_code=exam))


@app.command("quiz")
def quiz(
    domain: int = typer.Argument(..., help="Domain number to quiz (1-5)."),
    count: int = typer.Option(5, "--count", "-n", help="Number of questions."),
    exam: str | None = typer.Option(
        None, "--exam", "-e", help="Exam code. Auto-detects when only one exam is present."
    ),
) -> None:
    """Quick quiz on a specific domain."""
    import asyncio

    from cert_pepper.cli.study import run_study_session
    asyncio.run(run_study_session(domain=domain, count=count, use_ai=False, exam_code=exam))


@app.command("exam")
def exam_cmd(
    questions: int = typer.Option(90, "--questions", "-n", help="Number of questions."),
    time_limit: int = typer.Option(90, "--time", "-t", help="Time limit in minutes."),
    exam: str | None = typer.Option(
        None, "--exam", "-e", help="Exam code. Auto-detects when only one exam is present."
    ),
) -> None:
    """Run a timed mock exam (90 questions, 90 minutes)."""
    import asyncio

    from cert_pepper.cli.exam import run_exam
    asyncio.run(run_exam(total_questions=questions, time_limit_minutes=time_limit, exam_code=exam))


@app.command("progress")
def progress(
    exam: str | None = typer.Option(
        None, "--exam", "-e", help="Exam code. Auto-detects when only one exam is present."
    ),
) -> None:
    """Show progress dashboard: accuracy, predicted score, weak areas."""
    import asyncio

    from cert_pepper.cli.progress import show_dashboard
    asyncio.run(show_dashboard(exam_code=exam))


@app.command("upgrade")
def upgrade(
    skip_ingest: bool = typer.Option(False, "--skip-ingest", help="Skip content re-ingestion."),
    content_root: str | None = typer.Option(
        None, "--content-root", help="Override content root path."
    ),
) -> None:
    """Apply DB migrations and refresh study content. Safe to run on existing databases."""
    import asyncio

    from rich.console import Console
    from rich.table import Table

    from cert_pepper.config import Settings, get_settings
    from cert_pepper.db.connection import get_session, init_db
    from cert_pepper.ingestion.loader import run_ingestion

    console = Console()
    console.print("[cyan]Applying database migrations...[/cyan]")
    asyncio.run(init_db())
    console.print("[green]✓ Schema up to date[/green]")

    if not skip_ingest:
        settings = get_settings()
        if content_root:
            from pathlib import Path
            settings = Settings(content_root=Path(content_root))
        console.print(f"[cyan]Re-ingesting content from: {settings.content_root}[/cyan]")

        async def _run() -> dict[str, int]:
            async with get_session() as session:
                return await run_ingestion(session, settings)

        counts = asyncio.run(_run())
        table = Table(title="Content Updated", show_header=True)
        table.add_column("Type", style="cyan")
        table.add_column("Count", justify="right", style="green")
        table.add_row("Questions", str(counts["questions"]))
        table.add_row("Flashcards", str(counts["flashcards"]))
        table.add_row("Acronyms", str(counts["acronyms"]))
        console.print(table)

    console.print("[bold green]✓ Upgrade complete. Study progress preserved.[/bold green]")


@app.command("pregenerate")
def pregenerate(
    domain: int | None = typer.Option(
        None, "--domain", "-d", help="Only pregenerate for this domain."
    ),
) -> None:
    """Batch pre-generate AI explanations for all questions."""
    import asyncio

    from cert_pepper.cli.pregenerate import run_pregenerate
    asyncio.run(run_pregenerate(domain_filter=domain))


if __name__ == "__main__":
    app()
