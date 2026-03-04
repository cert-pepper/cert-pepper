"""CLI commands for managing study goals and viewing schedule progress."""

from __future__ import annotations

from datetime import date

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

app = typer.Typer(help="Set and view your exam study goal.", no_args_is_help=True)


@app.command("set")
def goal_set(
    exam_date: str = typer.Option(..., "--exam-date", help="Exam date (YYYY-MM-DD)."),
    hours: int = typer.Option(40, "--hours", help="Target study hours."),
    exam: str | None = typer.Option(
        None, "--exam", "-e", help="Exam code. Auto-detects when only one exam is present."
    ),
) -> None:
    """Set your exam date and study hour target."""
    import asyncio
    asyncio.run(_goal_set(exam_date, hours, exam))


@app.command("show")
def goal_show(
    exam: str | None = typer.Option(
        None, "--exam", "-e", help="Exam code. Auto-detects when only one exam is present."
    ),
) -> None:
    """Show schedule pace summary and study calendar."""
    import asyncio
    asyncio.run(_goal_show(exam))


async def _goal_set(exam_date_str: str, target_hours: int, exam_code: str | None) -> None:
    from sqlalchemy import text

    from cert_pepper.db.connection import get_session
    from cert_pepper.db.exams import resolve_cert_id
    from cert_pepper.db.goals import upsert_goal

    try:
        exam_date = date.fromisoformat(exam_date_str)
    except ValueError:
        console.print("[red]Invalid date format. Use YYYY-MM-DD.[/red]")
        raise typer.Exit(1)

    if exam_date <= date.today():
        console.print("[red]Exam date must be in the future.[/red]")
        raise typer.Exit(1)

    async with get_session() as session:
        result = await session.execute(
            text("SELECT id FROM users WHERE username='default' LIMIT 1")
        )
        row = result.fetchone()
        if not row:
            console.print("[red]No user found. Run `cert-pepper db init` first.[/red]")
            return
        user_id = row[0]

        try:
            cert_id = await resolve_cert_id(session, exam_code)
        except ValueError as e:
            console.print(f"[red]{e}[/red]")
            return

        cert_result = await session.execute(
            text("SELECT code, name FROM certifications WHERE id = :cid"),
            {"cid": cert_id},
        )
        cert_row = cert_result.fetchone()
        cert_label = f"{cert_row[0]} — {cert_row[1]}" if cert_row else "Unknown"

        await upsert_goal(session, user_id, cert_id, exam_date, target_hours)
        await session.commit()

    days_remaining = (exam_date - date.today()).days
    console.print(
        Panel(
            f"[bold green]Goal saved![/bold green]\n\n"
            f"Exam: [cyan]{cert_label}[/cyan]\n"
            f"Date: [cyan]{exam_date}[/cyan]  ({days_remaining} days away)\n"
            f"Target: [cyan]{target_hours} hours[/cyan]\n\n"
            f"Run [bold]cert-pepper goal show[/bold] to see your schedule.",
            border_style="green",
        )
    )


async def _goal_show(exam_code: str | None) -> None:
    from datetime import timedelta

    from sqlalchemy import text

    from cert_pepper.db.connection import get_session
    from cert_pepper.db.exams import resolve_cert_id
    from cert_pepper.db.goals import (
        get_daily_session_counts,
        get_goal,
        get_hours_completed,
        get_sessions_today,
    )
    from cert_pepper.engine.scorer import compute_schedule_status, get_day_statuses

    async with get_session() as session:
        result = await session.execute(
            text("SELECT id FROM users WHERE username='default' LIMIT 1")
        )
        row = result.fetchone()
        if not row:
            console.print("[red]No user found. Run `cert-pepper db init` first.[/red]")
            return
        user_id = row[0]

        try:
            cert_id = await resolve_cert_id(session, exam_code)
        except ValueError as e:
            console.print(f"[red]{e}[/red]")
            return

        goal = await get_goal(session, user_id, cert_id)
        if goal is None:
            console.print(
                "[yellow]No goal set. Run:[/yellow]\n"
                "  [bold]cert-pepper goal set --exam-date YYYY-MM-DD[/bold]"
            )
            return

        hours_completed = await get_hours_completed(session, user_id, cert_id)
        sessions_today = await get_sessions_today(session, user_id, cert_id)
        daily_counts = await get_daily_session_counts(session, user_id, cert_id)

        cert_result = await session.execute(
            text("SELECT code, name FROM certifications WHERE id = :cid"),
            {"cid": cert_id},
        )
        cert_row = cert_result.fetchone()
        cert_label = f"{cert_row[0]} — {cert_row[1]}" if cert_row else "Unknown"

    exam_date = goal["exam_date"]
    target_hours = goal["target_hours"]

    # created_at may be a string or a datetime; parse to date
    created_raw = goal.get("created_at")
    if created_raw:
        try:
            start_date = date.fromisoformat(str(created_raw)[:10])
        except ValueError:
            start_date = None
    else:
        start_date = None

    status = compute_schedule_status(
        exam_date=exam_date,
        target_hours=target_hours,
        hours_completed=hours_completed,
        sessions_today=sessions_today,
        start_date=start_date,
    )

    # --- Section 1: Pace summary ---
    pct_int = int(status.pct_complete * 100)
    bar_filled = int(status.pct_complete * 20)
    bar = "█" * bar_filled + "░" * (20 - bar_filled)
    pace_color = "green" if status.on_pace else "yellow"

    pace_lines = (
        f"[bold]{cert_label}[/bold]\n"
        f"Exam in [cyan]{status.days_remaining}[/cyan] day(s) · "
        f"[cyan]{target_hours}h[/cyan] goal · "
        f"[cyan]{hours_completed:.1f}h[/cyan] done ({pct_int}%) · "
        f"Need [cyan]{status.hours_remaining:.1f}h[/cyan] more\n"
        f"Recommended: [{pace_color}]{status.sessions_per_day} session(s)/day[/{pace_color}]\n"
        f"[{pace_color}]{bar}[/{pace_color}] {pct_int}%"
    )
    console.print()
    console.print(Panel(pace_lines, title="Study Goal", border_style="cyan"))

    # --- Section 2: Calendar (last 4 weeks + remaining days) ---
    today = date.today()
    calendar_start = today - timedelta(weeks=4)
    day_statuses = get_day_statuses(
        daily_sessions=daily_counts,
        exam_date=exam_date,
        sessions_per_day=status.sessions_per_day,
        start_date=calendar_start,
    )

    # Build a week-grid table
    cal_table = Table(
        title="Study Calendar",
        show_header=True,
        header_style="bold",
        show_lines=False,
        padding=(0, 1),
    )
    cal_table.add_column("Week", style="dim", no_wrap=True)
    for day_name in ("Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"):
        cal_table.add_column(day_name, justify="center", no_wrap=True)

    # Group by ISO week
    weeks: dict[tuple[int, int], dict[int, str]] = {}
    for ds in day_statuses:
        iso = ds.date.isocalendar()
        week_key = (iso.year, iso.week)
        if week_key not in weeks:
            weeks[week_key] = {}
        weekday = iso.weekday  # 1=Mon … 7=Sun
        cell = _day_cell(ds)
        weeks[week_key][weekday] = cell

    for (yr, wk), cells in sorted(weeks.items()):
        # Week label: use the Monday of this week
        monday = date.fromisocalendar(yr, wk, 1)
        label = monday.strftime("%b %d")
        row = [label] + [cells.get(d, " ") for d in range(1, 8)]
        cal_table.add_row(*row)

    console.print(cal_table)
    console.print(
        "[dim]✓ met   ~ partial   ✗ missed   □ today   · future[/dim]"
    )

    # --- Section 3: Catch-up message ---
    missed = sum(1 for ds in day_statuses if ds.status == "missed")
    if not status.on_pace or missed > 0:
        console.print()
        if missed > 0:
            console.print(
                f"[yellow]⚠ {missed} missed day(s) detected. "
                f"Recalculated pace: "
                f"{status.sessions_per_day} session(s)/day to reach goal by exam date.[/yellow]"
            )
        else:
            console.print(
                f"[yellow]⚠ Behind pace. "
                f"Aim for {status.sessions_per_day} session(s)/day.[/yellow]"
            )
    else:
        console.print()
        console.print("[green]On pace![/green]")
    console.print()


def _day_cell(ds) -> str:  # type: ignore[no-untyped-def]
    """Return a Rich-formatted cell string for a DayStatus."""
    if ds.status == "met":
        return "[green]✓[/green]"
    if ds.status == "partial":
        return "[yellow]~[/yellow]"
    if ds.status == "missed":
        return "[red]✗[/red]"
    if ds.status == "today":
        return "[bold]□[/bold]"
    return "[dim]·[/dim]"
