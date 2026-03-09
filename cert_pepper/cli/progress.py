"""Progress dashboard CLI command."""

from __future__ import annotations

from datetime import date as date_type

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from sqlalchemy import text

from cert_pepper.db.connection import get_session
from cert_pepper.engine.scorer import (
    compute_streak,
    get_question_counts,
    get_recommendations,
    get_weak_areas,
    predict_score,
)

console = Console()

MIN_DOMAIN_COVERAGE = 0.50


def domain_status_label(acc: float, attempts: int, total_questions: int) -> str:
    """Return Rich-markup status string for a domain row.

    'Mastered' is only shown when coverage (attempts / total_questions) has
    reached MIN_DOMAIN_COVERAGE; below that threshold high accuracy shows
    'On Track' instead, since the sample is too small to be conclusive.
    """
    coverage = attempts / total_questions if total_questions > 0 else 0.0
    if acc >= 0.85 and coverage >= MIN_DOMAIN_COVERAGE:
        return "[green]✓ Mastered[/green]"
    elif acc >= 0.70:
        return "[yellow]~ On Track[/yellow]"
    else:
        return "[red]✗ Weak[/red]"


async def show_dashboard(exam_code: str | None = None) -> None:
    """Render the full progress dashboard."""
    from cert_pepper.db.exams import resolve_cert_id

    async with get_session() as session:
        # Get default user
        result = await session.execute(
            text("SELECT id FROM users WHERE username='default' LIMIT 1")
        )
        row = result.fetchone()
        if not row:
            console.print("[red]No user found. Run `cert-pepper db init` first.[/red]")
            return
        user_id = row[0]

        # Resolve certification
        try:
            cert_id = await resolve_cert_id(session, exam_code)
        except ValueError as e:
            console.print(f"[red]{e}[/red]")
            return

        # Get cert info for subtitle
        result = await session.execute(
            text("SELECT code, name FROM certifications WHERE id = :cid"),
            {"cid": cert_id},
        )
        cert_row = result.fetchone()
        cert_label = f"{cert_row[0]} — {cert_row[1]}" if cert_row else "Unknown Exam"

        # Get domain names/weights from DB
        result = await session.execute(
            text(
                "SELECT number, name, weight_pct FROM domains"
                " WHERE certification_id = :cid ORDER BY number"
            ),
            {"cid": cert_id},
        )
        domain_rows = result.fetchall()
        domain_names = {row[0]: row[1] for row in domain_rows}
        domain_weights = {row[0]: int(row[2]) for row in domain_rows}

        # Get overall stats
        result = await session.execute(
            text("""
                SELECT COUNT(*) as total, SUM(is_correct) as correct
                FROM question_attempts WHERE user_id=:uid
            """),
            {"uid": user_id},
        )
        stats = result.fetchone()
        assert stats is not None
        total_attempts = stats[0] or 0
        total_correct = stats[1] or 0

        # Get domain breakdown (cert-scoped)
        result = await session.execute(
            text("""
                SELECT d.number, COUNT(*) as total, SUM(qa.is_correct) as correct
                FROM question_attempts qa
                JOIN questions q ON q.id = qa.question_id
                JOIN domains d ON d.id = q.domain_id
                WHERE qa.user_id = :uid
                AND d.certification_id = :cert_id
                GROUP BY d.number
                ORDER BY d.number
            """),
            {"uid": user_id, "cert_id": cert_id},
        )
        domain_stats = {row[0]: (row[1], row[2]) for row in result.fetchall()}

        # Total questions per domain (for coverage threshold check)
        result = await session.execute(
            text("""
                SELECT d.number, COUNT(*) as total
                FROM questions q
                JOIN domains d ON d.id = q.domain_id
                WHERE d.certification_id = :cert_id
                GROUP BY d.number
            """),
            {"cert_id": cert_id},
        )
        domain_totals = {row[0]: row[1] for row in result.fetchall()}

        # Get predicted score and question coverage
        score = await predict_score(session, user_id, cert_id=cert_id)
        counts = await get_question_counts(session, user_id, cert_id=cert_id)
        await get_weak_areas(session, user_id, cert_id=cert_id)
        recommendations = await get_recommendations(session, user_id, cert_id=cert_id)

        # Get FSRS cards due
        result = await session.execute(
            text("""
                SELECT COUNT(*) FROM fsrs_cards
                WHERE user_id=:uid AND due_date <= CURRENT_TIMESTAMP
            """),
            {"uid": user_id},
        )
        cards_row = result.fetchone()
        cards_due = cards_row[0] if cards_row else 0

        # Get study streak
        result = await session.execute(
            text("""
                SELECT DISTINCT date(started_at) as study_date
                FROM study_sessions
                WHERE user_id=:uid AND questions_seen > 0
                ORDER BY study_date DESC
            """),
            {"uid": user_id},
        )
        study_dates = [date_type.fromisoformat(row[0]) for row in result.fetchall()]
        streak = compute_streak(study_dates)

    # === Render Dashboard ===
    console.print()
    console.print(
        Panel(
            "[bold cyan]cert-pepper Progress Dashboard[/bold cyan]",
            subtitle=cert_label,
            border_style="cyan",
        )
    )

    # Schedule section (shown only when a goal is set)
    async with get_session() as session:
        from cert_pepper.db.goals import get_goal, get_hours_completed, get_sessions_today
        from cert_pepper.engine.scorer import compute_schedule_status

        goal = await get_goal(session, user_id, cert_id)
        if goal is not None:
            hours_completed = await get_hours_completed(session, user_id, cert_id)
            sessions_today_count = await get_sessions_today(session, user_id, cert_id)

            created_raw = goal.get("created_at")
            start_date = None
            if created_raw:
                try:
                    from datetime import date as date_cls
                    start_date = date_cls.fromisoformat(str(created_raw)[:10])
                except ValueError:
                    pass

            sched = compute_schedule_status(
                exam_date=goal["exam_date"],
                target_hours=goal["target_hours"],
                hours_completed=hours_completed,
                sessions_today=sessions_today_count,
                start_date=start_date,
            )
            pct_int = int(sched.pct_complete * 100)
            bar_filled = int(sched.pct_complete * 20)
            bar = "█" * bar_filled + "░" * (20 - bar_filled)
            pace_color = "green" if sched.on_pace else "yellow"
            console.print(
                f"[dim]Schedule:[/dim] Exam in [cyan]{sched.days_remaining}[/cyan] day(s) · "
                f"[cyan]{hours_completed:.1f}h[/cyan] / [cyan]{sched.target_hours}h[/cyan] · "
                f"[{pace_color}]{bar}[/{pace_color}] {pct_int}% · "
                f"[{pace_color}]{sched.sessions_per_day} session(s)/day recommended[/{pace_color}]"
            )
            console.print()
        else:
            console.print(
                "[dim]Tip: Run [bold]cert-pepper goal set --exam-date YYYY-MM-DD[/bold] "
                "to enable schedule tracking.[/dim]"
            )
            console.print()

    # Overall stats
    overall_acc = total_correct / total_attempts if total_attempts > 0 else 0
    score_color = (
        "green" if score.predicted_score >= 750
        else "yellow" if score.predicted_score >= 680
        else "red"
    )

    stats_table = Table(show_header=False, box=None, padding=(0, 2))
    stats_table.add_column("", style="dim")
    stats_table.add_column("")
    stats_table.add_row("Total Questions", f"{counts.total:,}")
    stats_table.add_row("  New (never seen)", f"[dim]{counts.new:,}[/dim]")
    stats_table.add_row("  Correct (≥1 right)", f"[green]{counts.correct:,}[/green]")
    stats_table.add_row(
        "  Incorrect (never right)",
        f"[red]{counts.incorrect:,}[/red]" if counts.incorrect > 0 else "0",
    )
    cov_color = (
        "green" if score.coverage_pct >= 0.5
        else "yellow" if score.coverage_pct >= 0.3
        else "red"
    )
    stats_table.add_row(
        "  Coverage",
        f"[{cov_color}]{score.coverage_pct:.0%} seen[/{cov_color}]",
    )
    stats_table.add_row("Overall Accuracy", f"{overall_acc:.1%}")
    stats_table.add_row(
        "Predicted Score",
        f"[{score_color}]{score.predicted_score}/900[/{score_color}] "
        f"(Pass prob: {score.pass_probability:.0%})",
    )
    stats_table.add_row(
        "Cards Due Today", f"[yellow]{cards_due}[/yellow]" if cards_due > 0 else "0"
    )
    stats_table.add_row("Study Streak", f"{streak} day{'s' if streak != 1 else ''}")
    console.print(stats_table)
    console.print()

    # Domain breakdown
    domain_table = Table(title="Domain Performance", show_header=True)
    domain_table.add_column("Domain", style="cyan")
    domain_table.add_column("Weight", justify="center")
    domain_table.add_column("Attempts", justify="right")
    domain_table.add_column("Correct", justify="right")
    domain_table.add_column("Accuracy", justify="right")
    domain_table.add_column("Status", justify="center")

    for num in sorted(domain_names.keys()):
        name = domain_names[num]
        weight = domain_weights[num]
        if num in domain_stats:
            total, correct = domain_stats[num]
            correct = correct or 0
            acc = correct / total if total > 0 else 0
            acc_str = f"{acc:.0%}"
            domain_total = domain_totals.get(num, 0)
            status = domain_status_label(acc, total, domain_total)
            if "Mastered" in status:
                acc_color = "green"
            elif "On Track" in status:
                acc_color = "yellow"
            else:
                acc_color = "red"
            domain_table.add_row(
                f"D{num}: {name[:30]}",
                f"{weight}%",
                str(total),
                str(correct),
                f"[{acc_color}]{acc_str}[/{acc_color}]",
                status,
            )
        else:
            domain_table.add_row(
                f"D{num}: {name[:30]}",
                f"{weight}%",
                "0",
                "0",
                "[dim]—[/dim]",
                "[dim]Not started[/dim]",
            )

    console.print(domain_table)
    console.print()

    # Recommendations
    if recommendations:
        rec_table = Table(title="Study Recommendations", show_header=True)
        rec_table.add_column("Priority", justify="center")
        rec_table.add_column("Domain", style="cyan")
        rec_table.add_column("Reason")
        rec_table.add_column("Time", justify="right")

        urgency_colors = {"critical": "red", "high": "yellow", "medium": "cyan", "low": "dim"}

        for i, rec in enumerate(recommendations[:5], 1):
            color = urgency_colors.get(rec.urgency, "white")
            rec_table.add_row(
                f"[{color}]#{i} {rec.urgency.upper()}[/{color}]",
                f"D{rec.domain_number}: {rec.domain_name[:30]}",
                rec.reason,
                f"{rec.suggested_minutes}min",
            )
        console.print(rec_table)
    else:
        console.print("[green]No weak areas detected. Great work![/green]")

    # Exam readiness
    console.print()
    MIN_COVERAGE = 0.50
    if score.coverage_pct < MIN_COVERAGE:
        console.print(
            f"[bold yellow]Exam Readiness: TOO EARLY TO TELL[/bold yellow] — "
            f"Only {score.coverage_pct:.0%} of questions seen "
            f"({counts.new} unseen). See more questions before relying on this score."
        )
    elif score.predicted_score >= 750:
        console.print(
            f"[bold green]Exam Readiness: READY[/bold green] — "
            f"Predicted {score.predicted_score}/900 (passing is 750)"
        )
    else:
        points_needed = 750 - score.predicted_score
        console.print(
            f"[bold yellow]Exam Readiness: NEEDS WORK[/bold yellow] — "
            f"Need {points_needed} more points. Focus on high-weight domains!"
        )
    console.print()
