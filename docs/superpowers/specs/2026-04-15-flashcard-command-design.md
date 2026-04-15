# Flashcard Command Design Spec

## Goal

Add a `cert-pepper flashcard` CLI command that lets users review flashcards one at a time, showing the front (term) and answer together on a single panel, with a tip below the answer if one exists. No rating or spaced repetition tracking — pure sequential review with shuffle.

## Architecture

One new file: `cert_pepper/cli/flashcards.py` — contains the `run_flashcard_session()` async function. The `main.py` registers a new `flashcard` Typer command that calls it via `asyncio.run()`.

No new DB tables, no FSRS writes, no BKT writes. The flashcard session is read-only against the DB.

## CLI Interface

```
cert-pepper flashcard [OPTIONS]

Options:
  -e, --exam TEXT        Exam code (e.g. CY0-001). Auto-detects if only one exam present.
  -d, --domain INTEGER   Filter to a specific domain number.
  -c, --category TEXT    Filter to a specific category (e.g. "AI Attacks").
  -n, --count INTEGER    Max cards to show per session. Default: all matching cards.
  --help
```

## Display

Each card renders as a single panel:

```
┌─────────────────────────────────────────────────────────────┐
│  Flashcard 3/106  ·  Domain 1  ·  AI Fundamentals          │
│                                                             │
│  What is differential privacy?                             │
│                                                             │
│  ─────────────────────────────────────────────────────────  │
│                                                             │
│  A mathematical guarantee that individual records cannot   │
│  be inferred from query results by adding calibrated       │
│  noise to outputs.                                         │
│                                                             │
│  💡 "Differential" = the difference one record makes       │
│     is undetectable                                        │
└─────────────────────────────────────────────────────────────┘
  [Enter] Next   [Q] Quit
```

- Header: card index / total, domain number, category
- Front (term) in bold
- Horizontal rule separator
- Answer in normal text
- Tip line prefixed with 💡, shown only when tip is non-empty
- Prompt at bottom: Enter to advance, Q to quit

## Data Flow

1. Resolve `cert_id` from exam code (same `resolve_cert_id()` helper used elsewhere)
2. Query `flashcards` joined to `domains` with optional `domain_id` and `category` filters
3. Shuffle the result list with `random.shuffle()`
4. Apply `count` cap if provided
5. Render each card; prompt for input

## Error Cases

- No flashcards found for the given filters: print a message and exit cleanly
- Unknown exam code: print error and exit (same pattern as study command)

## Testing

- `TestFlashcardSession` in `tests/test_flashcards.py`
- `test_run_flashcard_session_shows_all_cards` — seeds 3 flashcards, mocks `Prompt.ask`, asserts session completes without error
- `test_run_flashcard_session_domain_filter` — seeds cards in two domains, filters to one, asserts only correct cards shown
- `test_run_flashcard_session_category_filter` — seeds cards in two categories, filters to one
- `test_run_flashcard_session_count_cap` — seeds 5 cards, count=2, asserts only 2 shown
- `test_run_flashcard_session_no_cards_exits_cleanly` — empty DB, asserts graceful exit message
