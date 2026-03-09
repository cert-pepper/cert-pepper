"""Interactive study session with Rich TUI."""

from __future__ import annotations

import time
from datetime import datetime

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
from rich.text import Text
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from cert_pepper.db.connection import get_session
from cert_pepper.engine import fsrs, selector
from cert_pepper.engine.bkt import BKTParams
from cert_pepper.engine.bkt import update as bkt_update
from cert_pepper.models.content import Question

console = Console()

RATING_LABELS = {
    1: "[red]Again[/red]",
    2: "[yellow]Hard[/yellow]",
    3: "[green]Good[/green]",
    4: "[blue]Easy[/blue]",
}


async def get_default_user_id(session: AsyncSession) -> int:
    result = await session.execute(text("SELECT id FROM users WHERE username='default' LIMIT 1"))
    row = result.fetchone()
    if row:
        return int(row[0])
    await session.execute(text("INSERT OR IGNORE INTO users (username) VALUES ('default')"))
    result = await session.execute(text("SELECT id FROM users WHERE username='default' LIMIT 1"))
    final_row = result.fetchone()
    return int(final_row[0]) if final_row else 1


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


async def get_or_create_fsrs_card(
    session: AsyncSession, user_id: int, question_id: int
) -> fsrs.FSRSCard:
    result = await session.execute(
        text("""
            SELECT stability, difficulty, retrievability, due_date,
                   last_review, state, step, reps, lapses
            FROM fsrs_cards
            WHERE user_id=:uid AND content_type='question' AND content_id=:qid
        """),
        {"uid": user_id, "qid": question_id},
    )
    row = result.fetchone()
    if row:
        return fsrs.FSRSCard(
            stability=row[0],
            difficulty=row[1],
            retrievability=row[2],
            due_date=datetime.fromisoformat(str(row[3])),
            last_review=datetime.fromisoformat(str(row[4])) if row[4] else None,
            state=row[5],
            step=row[6],
            reps=row[7],
            lapses=row[8],
        )
    return fsrs.FSRSCard()


async def save_fsrs_card(
    session: AsyncSession, user_id: int, question_id: int, card: fsrs.FSRSCard
) -> None:
    await session.execute(
        text("""
            INSERT INTO fsrs_cards
                (user_id, content_type, content_id, stability, difficulty, retrievability,
                 due_date, last_review, state, step, reps, lapses)
            VALUES (:uid, 'question', :qid, :s, :d, :r, :due, :last, :state, :step, :reps, :lapses)
            ON CONFLICT(user_id, content_type, content_id) DO UPDATE SET
                stability=excluded.stability,
                difficulty=excluded.difficulty,
                retrievability=excluded.retrievability,
                due_date=excluded.due_date,
                last_review=excluded.last_review,
                state=excluded.state,
                step=excluded.step,
                reps=excluded.reps,
                lapses=excluded.lapses
        """),
        {
            "uid": user_id,
            "qid": question_id,
            "s": card.stability,
            "d": card.difficulty,
            "r": card.retrievability,
            "due": card.due_date.isoformat(),
            "last": card.last_review.isoformat() if card.last_review else None,
            "state": card.state,
            "step": card.step,
            "reps": card.reps,
            "lapses": card.lapses,
        },
    )


async def update_bkt(
    session: AsyncSession, user_id: int, domain_id: int, is_correct: bool
) -> None:
    result = await session.execute(
        text("""
            SELECT p_mastery, p_learn, p_guess, p_slip, attempts, correct
            FROM bkt_skill_states
            WHERE user_id=:uid AND skill_id=:sid AND skill_type='domain'
        """),
        {"uid": user_id, "sid": domain_id},
    )
    row = result.fetchone()
    if row:
        params = BKTParams(
            p_mastery=row[0], p_learn=row[1], p_guess=row[2],
            p_slip=row[3], attempts=row[4], correct=row[5],
        )
    else:
        params = BKTParams()

    updated = bkt_update(params, is_correct)

    await session.execute(
        text("""
            INSERT INTO bkt_skill_states
                (user_id, skill_id, skill_type, p_mastery, p_learn, p_guess, p_slip,
                 attempts, correct, accuracy_pct)
            VALUES (:uid, :sid, 'domain', :pm, :pl, :pg, :ps, :att, :cor, :acc)
            ON CONFLICT(user_id, skill_id, skill_type) DO UPDATE SET
                p_mastery=excluded.p_mastery,
                attempts=excluded.attempts,
                correct=excluded.correct,
                accuracy_pct=excluded.accuracy_pct,
                updated_at=CURRENT_TIMESTAMP
        """),
        {
            "uid": user_id, "sid": domain_id,
            "pm": updated.p_mastery, "pl": updated.p_learn,
            "pg": updated.p_guess, "ps": updated.p_slip,
            "att": updated.attempts, "cor": updated.correct,
            "acc": updated.accuracy_pct,
        },
    )


def display_question(q: Question, q_num: int, total: int) -> None:
    """Render question with Rich panel."""
    domain_colors = {1: "blue", 2: "red", 3: "green", 4: "yellow", 5: "magenta"}
    color = domain_colors.get(q.domain_number, "white")

    header = f"[{color}]Domain {q.domain_number}[/{color}]  |  Question {q_num}/{total}"
    panel_content = Text(q.stem + "\n")

    console.print()
    console.print(Panel(panel_content, title=header, border_style=color))

    for letter, text_val in q.options_dict().items():
        console.print(f"  [bold]{letter})[/bold] {text_val}")
    console.print()


def get_answer_from_user(use_ai: bool = True) -> tuple[str, bool]:
    """Get answer from user. Returns (answer, hint_used)."""
    hint_used = False

    while True:
        prompt_text = "Your answer [A/B/C/D"
        if use_ai:
            prompt_text += "/H=hint"
        prompt_text += "/Q=quit]: "

        ans = Prompt.ask(prompt_text).strip().upper()

        if ans == "Q":
            raise KeyboardInterrupt

        if ans == "H" and use_ai:
            hint_used = True
            console.print("[dim]Generating hint...[/dim]")
            return "HINT", True  # caller handles hint generation

        if ans in ("A", "B", "C", "D"):
            return ans, hint_used

        console.print("[red]Please enter A, B, C, or D.[/red]")


def get_fsrs_rating() -> int:
    """Ask user to rate recall difficulty after showing answer."""
    console.print(
        "\n[dim]How well did you know this?[/dim]\n"
        "  [red]1) Again[/red] — didn't know\n"
        "  [yellow]2) Hard[/yellow] — barely remembered\n"
        "  [green]3) Good[/green] — knew it\n"
        "  [blue]4) Easy[/blue] — knew it instantly\n"
    )
    while True:
        rating_str = Prompt.ask("Rating", choices=["1", "2", "3", "4"], default="3")
        return int(rating_str)


async def run_study_session(
    domain: int | None = None,
    count: int = 10,
    use_ai: bool = True,
    exam_code: str | None = None,
    new_only: bool = False,
) -> None:
    """Run an interactive study session."""
    console.print(
        Panel(
            "[bold cyan]cert-pepper Study Session[/bold cyan]\n"
            f"Domain: {f'Domain {domain}' if domain else 'Adaptive (all domains)'} | "
            f"Questions: {count}",
            border_style="cyan",
        )
    )

    async with get_session() as session:
        user_id = await get_default_user_id(session)

        # Resolve certification
        from cert_pepper.db.exams import resolve_cert_id
        try:
            cert_id = await resolve_cert_id(session, exam_code)
        except ValueError as e:
            console.print(f"[red]{e}[/red]")
            return

        # Create study session record
        await session.execute(
            text("""
                INSERT INTO study_sessions (user_id, session_type, domain_filter, certification_id)
                VALUES (:uid, 'study', :domain, :cert_id)
            """),
            {"uid": user_id, "domain": domain, "cert_id": cert_id},
        )
        session_id_result = await session.execute(
            text("SELECT last_insert_rowid()")
        )
        id_row = session_id_result.fetchone()
        session_id = int(id_row[0]) if id_row else 0

        correct_count = 0
        seen_count = 0
        start_time = time.time()

        for i in range(count):
            # Select next question
            question_id = await selector.select_question(
                session, user_id, domain_filter=domain, cert_id=cert_id, new_only=new_only
            )
            if question_id is None:
                console.print("[yellow]No more questions available![/yellow]")
                break

            q = await get_question(session, question_id)
            if q is None:
                continue

            display_question(q, i + 1, count)

            # Get answer
            hint_used = False
            q_start = time.time()

            while True:
                try:
                    answer, hint_requested = get_answer_from_user(use_ai=use_ai)
                except KeyboardInterrupt:
                    console.print("\n[yellow]Session ended early.[/yellow]")
                    break

                if answer == "HINT" and use_ai:
                    # Generate hint
                    try:
                        from cert_pepper.ai.client import generate_hint
                        hint = generate_hint(q.stem, q.options_dict())
                        console.print(Panel(f"[dim]{hint}[/dim]", title="Hint", border_style="dim"))
                        hint_used = True
                    except Exception as e:
                        console.print(f"[red]Could not generate hint: {e}[/red]")
                    continue

                break
            else:
                # KeyboardInterrupt inner loop — break outer
                break

            time_taken = time.time() - q_start
            is_correct = answer == q.correct_answer

            # Show result
            if is_correct:
                console.print("\n[bold green]✓ Correct![/bold green]")
                correct_count += 1
            else:
                console.print(
                    f"\n[bold red]✗ Incorrect.[/bold red] "
                    f"The correct answer was "
                    f"[bold]{q.correct_answer}) {q.get_option(q.correct_answer)}[/bold]"
                )

            # Show explanation
            if q.explanation:
                console.print(Panel(q.explanation, title="Explanation", border_style="dim"))
            elif use_ai and not is_correct:
                try:
                    from cert_pepper.ai.explainer import get_explanation
                    explanation = await get_explanation(session, q, answer)
                    console.print(Panel(explanation, title="[AI] Explanation", border_style="dim"))
                except Exception:
                    pass  # silently skip AI on error

            # Get FSRS rating
            rating = get_fsrs_rating()

            # Update FSRS
            card = await get_or_create_fsrs_card(session, user_id, question_id)
            updated_card = fsrs.schedule(card, rating)
            await save_fsrs_card(session, user_id, question_id, updated_card)

            # Update BKT
            await update_bkt(session, user_id, q.domain_id, is_correct)

            # Record attempt
            await session.execute(
                text("""
                    INSERT INTO question_attempts
                        (session_id, user_id, question_id, selected_answer, is_correct,
                         time_taken_seconds, hint_used)
                    VALUES (:sid, :uid, :qid, :ans, :correct, :time, :hint)
                """),
                {
                    "sid": session_id,
                    "uid": user_id,
                    "qid": question_id,
                    "ans": answer,
                    "correct": 1 if is_correct else 0,
                    "time": time_taken,
                    "hint": 1 if hint_used else 0,
                },
            )

            seen_count += 1

            # Show progress bar hint
            accuracy = correct_count / seen_count if seen_count > 0 else 0
            bar_filled = int(accuracy * 20)
            bar = "█" * bar_filled + "░" * (20 - bar_filled)
            console.print(
                f"[dim]Progress: {seen_count}/{count} | "
                f"Accuracy: {bar} {accuracy:.0%}[/dim]"
            )
            console.print()

        # End session
        total_time = int(time.time() - start_time)
        await session.execute(
            text("""
                UPDATE study_sessions SET
                    ended_at=CURRENT_TIMESTAMP,
                    questions_seen=:seen,
                    questions_correct=:correct,
                    total_time_seconds=:time
                WHERE id=:sid
            """),
            {
                "seen": seen_count,
                "correct": correct_count,
                "time": total_time,
                "sid": session_id,
            },
        )

        # Update daily_progress aggregate
        study_minutes = total_time // 60
        await session.execute(
            text("""
                INSERT INTO daily_progress
                    (user_id, date, questions_seen, questions_correct, study_minutes)
                VALUES (:uid, DATE('now'), :seen, :correct, :minutes)
                ON CONFLICT(user_id, date) DO UPDATE SET
                    questions_seen = questions_seen + excluded.questions_seen,
                    questions_correct = questions_correct + excluded.questions_correct,
                    study_minutes = study_minutes + excluded.study_minutes
            """),
            {
                "uid": user_id,
                "seen": seen_count,
                "correct": correct_count,
                "minutes": study_minutes,
            },
        )

    # Final summary
    accuracy = correct_count / seen_count if seen_count > 0 else 0
    table = Table(title="Session Summary", show_header=False)
    table.add_column("Metric", style="cyan")
    table.add_column("Value", justify="right")
    table.add_row("Questions", f"{seen_count}/{count}")
    table.add_row("Correct", str(correct_count))
    table.add_row("Accuracy", f"{accuracy:.0%}")
    table.add_row("Time", f"{total_time // 60}m {total_time % 60}s")

    console.print()
    console.print(table)
    console.print(
        f'[dim]Session ID: {session_id} — '
        f'Ask Claude: "Explain my wrong answers from session {session_id}"[/dim]'
    )

    if accuracy >= 0.85:
        console.print(
            "[bold green]Excellent! You're well above the mastery threshold.[/bold green]"
        )
    elif accuracy >= 0.70:
        console.print("[yellow]Good progress! Keep practicing to reach 85%+.[/yellow]")
    else:
        console.print("[red]Keep studying — focus on the domains where you struggled.[/red]")
