"""Mock exam CLI: 90 questions, timed, with per-domain breakdown."""

from __future__ import annotations

import math
import signal
import sys
import threading
import time

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from cert_pepper.db.connection import get_session
from cert_pepper.engine import selector
from cert_pepper.engine.selector import count_unseen_questions
from cert_pepper.models.content import Question

console = Console()


class _TimeUpError(Exception):
    """Raised by SIGALRM when the exam time limit expires."""


def _sigalrm_handler(signum: int, frame: object) -> None:  # noqa: ARG001
    raise _TimeUpError()


async def get_question(session: AsyncSession, question_id: int) -> Question | None:
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


def _timer_thread(
    start_time: float,
    time_limit_seconds: float,
    stop_event: threading.Event,
    lines_above: int = 1,
) -> None:
    """Rewrite the timer line (lines_above lines above cursor) every second."""
    while True:
        elapsed = time.time() - start_time
        remaining = max(0.0, time_limit_seconds - elapsed)
        time_str = format_time(int(remaining))
        if remaining > 1800:
            color = "\033[32m"   # green
        elif remaining > 600:
            color = "\033[33m"   # yellow
        else:
            color = "\033[31m"   # red
        reset = "\033[0m"
        # Save cursor, move up to timer line, clear and rewrite, restore cursor
        sys.stdout.write(
            f"\033[s\033[{lines_above}A\r\033[2K{color}  Time remaining: {time_str}{reset}\033[u"
        )
        sys.stdout.flush()
        if stop_event.wait(1.0):
            break


async def run_exam(
    total_questions: int = 90,
    time_limit_minutes: int = 90,
    exam_code: str | None = None,
) -> None:
    """Run a timed mock exam."""
    console.print()
    console.print(
        Panel(
            f"[bold cyan]cert-pepper Mock Exam[/bold cyan]\n\n"
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
        result = await session.execute(
            text("SELECT id FROM users WHERE username='default' LIMIT 1")
        )
        row = result.fetchone()
        if not row:
            console.print("[red]No user found. Run `cert-pepper db init` first.[/red]")
            return
        user_id = row[0]

        # Resolve certification
        from cert_pepper.db.exams import resolve_cert_id
        try:
            cert_id = await resolve_cert_id(session, exam_code)
        except ValueError as e:
            console.print(f"[red]{e}[/red]")
            return

        # Fetch domain names and weights from DB
        result = await session.execute(
            text(
                "SELECT number, name, weight_pct FROM domains"
                " WHERE certification_id = :cid ORDER BY number"
            ),
            {"cid": cert_id},
        )
        domain_rows = result.fetchall()
        domain_names = {row[0]: row[1] for row in domain_rows}
        domain_weights = {row[0]: row[2] / 100.0 for row in domain_rows}

        # Select exam questions proportionally
        question_ids = await selector.select_exam_questions(
            session, user_id, total=total_questions, cert_id=cert_id
        )

        if not question_ids:
            console.print("[red]No questions available. Run `cert-pepper ingest` first.[/red]")
            return

        actual_count = len(question_ids)
        unseen_count, total_pool = await count_unseen_questions(session, user_id, cert_id)
        seen_count = actual_count - min(unseen_count, actual_count)
        new_in_exam = min(unseen_count, actual_count)
        console.print(
            f"\n[cyan]{actual_count} questions selected"
            f" — {new_in_exam} new, {seen_count} previously seen[/cyan]\n"
        )

        # Create exam session
        await session.execute(
            text(
                "INSERT INTO study_sessions (user_id, session_type, certification_id)"
                " VALUES (:uid, 'exam', :cert_id)"
            ),
            {"uid": user_id, "cert_id": cert_id},
        )
        result = await session.execute(text("SELECT last_insert_rowid()"))
        session_row = result.fetchone()
        session_id = session_row[0] if session_row else 0

        # Track answers
        answers: dict[int, str] = {}  # question_id → selected answer
        questions: dict[int, Question] = {}
        domain_nums = sorted(domain_names.keys())
        domain_results: dict[int, list[bool]] = {n: [] for n in domain_nums}

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

            domain_colors = {1: "blue", 2: "red", 3: "green", 4: "yellow", 5: "magenta"}
            color = domain_colors.get(q.domain_number, "white")

            # Timer line first — thread will rewrite it in-place
            elapsed_now = time.time() - start_time
            remaining_now = max(0.0, time_limit_seconds - elapsed_now)
            time_str_now = format_time(int(remaining_now))
            time_color = (
                "\033[32m" if remaining_now > 1800
                else "\033[33m" if remaining_now > 600
                else "\033[31m"
            )
            sys.stdout.write(f"{time_color}  Time remaining: {time_str_now}\033[0m\n")
            sys.stdout.flush()

            # Question header, stem, options
            console.print(
                f"[dim]Question {i}/{actual_count} | "
                f"[{color}]Domain {q.domain_number}[/{color}][/dim]"
            )
            console.print(f"\n{q.stem}\n")
            for letter, text_val in q.options_dict().items():
                console.print(f"  [bold]{letter})[/bold] {text_val}")
            console.print()

            # Estimate how many lines down the prompt is from the timer line so the
            # thread knows how far up to jump.  Components after the timer row:
            #   1  header line
            #   1  blank line before stem  (from leading \n in f"\n{stem}\n")
            #   stem_lines  wrapped stem text
            #   2  blank lines after stem  (trailing \n in f-string + Rich's own \n)
            #   opt_lines  option rows
            #   1  blank line  (console.print())
            console_width = console.width or 80
            stem_lines = max(1, math.ceil(len(q.stem) / (console_width - 2)))
            opt_lines = sum(
                max(1, math.ceil((4 + len(text_val)) / (console_width - 2)))
                for text_val in q.options_dict().values()
            )
            lines_above = 1 + 1 + stem_lines + 2 + opt_lines + 1

            # Set SIGALRM to fire exactly when the time limit expires
            alarm_secs = max(1, math.ceil(time_limit_seconds - (time.time() - start_time)))
            signal.signal(signal.SIGALRM, _sigalrm_handler)
            signal.alarm(alarm_secs)

            # Start live-timer thread
            stop_timer = threading.Event()
            timer_t = threading.Thread(
                target=_timer_thread,
                args=(start_time, time_limit_seconds, stop_timer, lines_above),
                daemon=True,
            )
            timer_t.start()

            # Get answer — _TimeUpError raised by SIGALRM interrupts Prompt.ask()
            ans = ""
            try:
                while True:
                    ans = Prompt.ask("Answer [A/B/C/D/Q=quit]").strip().upper()
                    if ans == "Q":
                        console.print("\n[yellow]Exam ended early.[/yellow]")
                        break
                    if ans in ("A", "B", "C", "D"):
                        answers[q_id] = ans
                        is_correct = ans == q.correct_answer
                        if q.domain_number in domain_results:
                            domain_results[q.domain_number].append(is_correct)
                        console.print("[dim]Recorded.[/dim]\n")
                        break
                    console.print("[red]Enter A, B, C, D, or Q.[/red]")
            except _TimeUpError:
                console.print("\n[bold red]Time's up![/bold red]")
                ans = "Q"
            finally:
                signal.alarm(0)  # cancel any pending alarm
                stop_timer.set()
                timer_t.join(timeout=2.0)

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

    for num in sorted(domain_names.keys()):
        name = domain_names.get(num, f"Domain {num}")
        weight = domain_weights.get(num, 0.0)
        results = domain_results.get(num, [])
        if results:
            d_correct = sum(results)
            d_total = len(results)
            d_acc = d_correct / d_total
            acc_color = "green" if d_acc >= 0.75 else "yellow" if d_acc >= 0.60 else "red"
            domain_table.add_row(
                f"D{num}: {name[:30]}",
                f"{weight:.0%}",
                str(d_total),
                str(d_correct),
                f"[{acc_color}]{d_acc:.0%}[/{acc_color}]",
            )
        else:
            domain_table.add_row(
                f"D{num}: {name[:30]}",
                f"{weight:.0%}",
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
                    name = domain_names.get(num, f"Domain {num}")
                    console.print(
                        f"  • Domain {num}: {name} — {acc:.0%} accuracy"
                    )

    console.print(
        f'[dim]Session ID: {session_id} — '
        f'Ask Claude: "Explain my wrong answers from session {session_id}"[/dim]'
    )
    console.print()
