"""Mock exam CLI: 90 questions, timed, with per-domain breakdown."""

from __future__ import annotations

import asyncio
import time
from datetime import datetime

from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeElapsedColumn
from rich.table import Table
from rich.prompt import Prompt
from sqlalchemy import text

from cert_pepper.db.connection import get_session
from cert_pepper.engine import selector
from cert_pepper.models.content import Question

console = Console()

DOMAIN_NAMES = {
    1: "General Security Concepts",
    2: "Threats, Vulnerabilities & Mitigations",
    3: "Security Architecture",
    4: "Security Operations",
    5: "Program Management & Oversight",
}
DOMAIN_WEIGHTS = {1: 0.12, 2: 0.22, 3: 0.18, 4: 0.28, 5: 0.20}


async def get_question(session, question_id: int) -> Question | None:
    result = await session.execute(
        text("""
            SELECT q.id, q.domain_id, d.number, q.number, q.stem,
                   q.option_a, q.option_b, q.option_c, q.option_d,
                   q.correct_answer, q.explanation, q.difficulty, q.source_file
            FROM questions q
            JOIN domains d ON d.id = q.domain_id
            WHERE q.id = :qid
        """),
        {"qid": question_id},
    )
    row = result.fetchone()
    if not row:
        return None
    return Question(
        id=row[0], domain_id=row[1], domain_number=row[2], number=row[3],
        stem=row[4], option_a=row[5], option_b=row[6], option_c=row[7],
        option_d=row[8], correct_answer=row[9], explanation=row[10],
        difficulty=row[11], source_file=row[12],
    )


def format_time(seconds: int) -> str:
    m, s = divmod(seconds, 60)
    return f"{m:02d}:{s:02d}"


async def run_exam(total_questions: int = 90, time_limit_minutes: int = 90) -> None:
    """Run a timed mock exam."""
    console.print()
    console.print(
        Panel(
            f"[bold cyan]cert-pepper Mock Exam[/bold cyan]\n\n"
            f"Security+ SY0-701 Simulation\n"
            f"{total_questions} questions | {time_limit_minutes} minutes\n\n"
            f"[yellow]Press Q at any question to end the exam early.[/yellow]",
            border_style="cyan",
        )
    )

    confirm = Prompt.ask("\nReady to start? [Y/n]", default="Y")
    if confirm.upper() not in ("Y", ""):
        console.print("[yellow]Exam cancelled.[/yellow]")
        return

    async with get_session() as session:
        # Get user
        result = await session.execute(text("SELECT id FROM users WHERE username='default' LIMIT 1"))
        row = result.fetchone()
        if not row:
            console.print("[red]No user found. Run `cert-pepper db init` first.[/red]")
            return
        user_id = row[0]

        # Select exam questions proportionally
        question_ids = await selector.select_exam_questions(session, user_id, total=total_questions)

        if not question_ids:
            console.print("[red]No questions available. Run `cert-pepper ingest` first.[/red]")
            return

        actual_count = len(question_ids)
        console.print(f"\n[cyan]Starting exam with {actual_count} questions...[/cyan]\n")

        # Create exam session
        await session.execute(
            text("INSERT INTO study_sessions (user_id, session_type) VALUES (:uid, 'exam')"),
            {"uid": user_id},
        )
        result = await session.execute(text("SELECT last_insert_rowid()"))
        session_id = result.fetchone()[0]

        # Track answers
        answers: dict[int, str] = {}  # question_id → selected answer
        questions: dict[int, Question] = {}
        domain_results: dict[int, list[bool]] = {i: [] for i in range(1, 6)}

        start_time = time.time()
        time_limit_seconds = time_limit_minutes * 60
        i = 0

        for i, q_id in enumerate(question_ids, 1):
            # Check time remaining
            elapsed = time.time() - start_time
            remaining = time_limit_seconds - elapsed

            if remaining <= 0:
                console.print("\n[bold red]⏰ Time's up![/bold red]")
                break

            q = await get_question(session, q_id)
            if q is None:
                continue

            questions[q_id] = q

            # Display question with timer
            time_str = format_time(int(remaining))
            domain_colors = {1: "blue", 2: "red", 3: "green", 4: "yellow", 5: "magenta"}
            color = domain_colors.get(q.domain_number, "white")

            console.print(
                f"[dim]Question {i}/{actual_count} | "
                f"[{color}]Domain {q.domain_number}[/{color}] | "
                f"Time remaining: [{'green' if remaining > 1800 else 'yellow' if remaining > 600 else 'red'}]{time_str}[/]"
                f"[/dim]"
            )
            console.print(f"\n{q.stem}\n")
            for letter, text_val in q.options_dict().items():
                console.print(f"  [bold]{letter})[/bold] {text_val}")
            console.print()

            # Get answer
            while True:
                ans = Prompt.ask("Answer [A/B/C/D/Q=quit]").strip().upper()
                if ans == "Q":
                    console.print("\n[yellow]Exam ended early.[/yellow]")
                    goto_results = True
                    break
                if ans in ("A", "B", "C", "D"):
                    answers[q_id] = ans
                    is_correct = ans == q.correct_answer
                    domain_results[q.domain_number].append(is_correct)
                    console.print(f"[dim]Recorded.[/dim]\n")
                    break
                console.print("[red]Enter A, B, C, D, or Q.[/red]")
            else:
                goto_results = False

            if ans == "Q":
                break

        # Calculate results
        elapsed = int(time.time() - start_time)
        total_answered = len(answers)
        total_correct = sum(1 for q_id, ans in answers.items()
                           if questions.get(q_id) and ans == questions[q_id].correct_answer)

        # Save attempts
        for q_id, ans in answers.items():
            q = questions.get(q_id)
            if q:
                is_correct = ans == q.correct_answer
                await session.execute(
                    text("""
                        INSERT INTO question_attempts
                            (session_id, user_id, question_id, selected_answer, is_correct)
                        VALUES (:sid, :uid, :qid, :ans, :correct)
                    """),
                    {
                        "sid": session_id, "uid": user_id, "qid": q_id,
                        "ans": ans, "correct": 1 if is_correct else 0,
                    },
                )

        # Update session
        await session.execute(
            text("""
                UPDATE study_sessions SET
                    ended_at=CURRENT_TIMESTAMP,
                    questions_seen=:seen,
                    questions_correct=:correct,
                    total_time_seconds=:time
                WHERE id=:sid
            """),
            {"seen": total_answered, "correct": total_correct, "time": elapsed, "sid": session_id},
        )

    # === Results ===
    overall_acc = total_correct / total_answered if total_answered > 0 else 0
    # Security+ score: 100-900, linear mapping from 0% to 100%
    predicted_score = round(100 + overall_acc * 800)
    passed = predicted_score >= 750
    score_color = "green" if passed else "red"

    console.print()
    console.print(
        Panel(
            f"[bold]Mock Exam Results[/bold]\n\n"
            f"Score: [{score_color}]{predicted_score}/900[/{score_color}] "
            f"({'[green]PASS[/green]' if passed else '[red]FAIL[/red]'})\n"
            f"Answered: {total_answered}/{actual_count}\n"
            f"Correct: {total_correct}/{total_answered} ({overall_acc:.1%})\n"
            f"Time: {format_time(elapsed)}",
            border_style=score_color,
            title="Exam Complete",
        )
    )

    # Domain breakdown
    domain_table = Table(title="Domain Breakdown", show_header=True)
    domain_table.add_column("Domain", style="cyan")
    domain_table.add_column("Weight", justify="center")
    domain_table.add_column("Answered", justify="right")
    domain_table.add_column("Correct", justify="right")
    domain_table.add_column("Accuracy", justify="right")

    for num in range(1, 6):
        results = domain_results[num]
        if results:
            d_correct = sum(results)
            d_total = len(results)
            d_acc = d_correct / d_total
            acc_color = "green" if d_acc >= 0.75 else "yellow" if d_acc >= 0.60 else "red"
            domain_table.add_row(
                f"D{num}: {DOMAIN_NAMES[num][:30]}",
                f"{DOMAIN_WEIGHTS[num]:.0%}",
                str(d_total),
                str(d_correct),
                f"[{acc_color}]{d_acc:.0%}[/{acc_color}]",
            )
        else:
            domain_table.add_row(
                f"D{num}: {DOMAIN_NAMES[num][:30]}",
                f"{DOMAIN_WEIGHTS[num]:.0%}",
                "0", "0", "[dim]—[/dim]",
            )

    console.print(domain_table)

    if not passed:
        console.print(
            "\n[yellow]Focus areas for next study session:[/yellow]"
        )
        weak = sorted(
            [(num, results) for num, results in domain_results.items() if results],
            key=lambda x: sum(x[1]) / len(x[1]) if x[1] else 0,
        )
        for num, results in weak[:3]:
            if results:
                acc = sum(results) / len(results)
                if acc < 0.75:
                    console.print(
                        f"  • Domain {num}: {DOMAIN_NAMES[num]} — {acc:.0%} accuracy"
                    )

    console.print()
