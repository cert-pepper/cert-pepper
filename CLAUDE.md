# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Layout

```
cert-pepper/
├── cert_pepper/          — Python source (the app)
│   ├── cli/              — Typer commands
│   ├── mcp/              — Three FastMCP STDIO servers
│   ├── engine/           — FSRS, BKT, selector, scorer (pure Python, no DB deps)
│   ├── ingestion/        — Markdown parsers
│   ├── ai/               — Anthropic client + explainer
│   └── db/               — SQLAlchemy async engine + schema
├── tests/                — pytest suite
├── examples/
│   └── security-plus/    — Security+ SY0-701 exam content (read-only input)
├── docs/
│   ├── walkthrough.md    — 10-day Security+ study guide
│   └── content-format.md — Format spec for exam content
├── pyproject.toml
├── .env                  — Local config (not committed)
└── .env.example          — Config template
```

All development happens in `cert_pepper/` and `tests/`. Content under `examples/` is never modified by the app — it is read-only input.

## TDD Red-Green Workflow (Required)

**Every piece of code written in this repo must follow TDD red-green:**

1. **Write a failing test first** — run it to confirm it fails with the expected error (red).
2. **Write the minimal code to make it pass** — run again to confirm green.
3. **Refactor** if needed, keeping tests green.

This is not optional. Do not write production code before writing the test that exercises it. Tests must be legitimate — they should fail if the implementation is wrong, not just be structural boilerplate.

**Test file locations**: `tests/`. Each module in `cert_pepper/` has a corresponding `test_<module>.py`.

**Running tests**:
```bash
uv run pytest tests/test_fsrs.py -v              # single file
uv run pytest tests/test_fsrs.py::TestClass::test_name  # single test (run this to verify red before implementing)
uv run pytest                                     # full suite (must stay green)
```

**Test patterns used in this repo**:
- Pure functions: call directly, assert return values.
- Async DB tests: use the `db` fixture from `conftest.py` (patches `DB_PATH`, resets engine singletons, calls `init_db()`). Mark test class methods as `async def` — `asyncio_mode = "auto"` handles the event loop.
- Use `seed_question()`, `seed_attempt()`, `seed_session()`, `get_user_id()` from `conftest.py` to set up DB state.
- AI/API functions: test only the pure helpers (`make_prompt_hash`, `get_explainer_system`). Do not call live APIs in tests.

## Common Commands

All commands run from the repo root with `uv`. The `.env` file sets `DB_PATH` and `CONTENT_ROOT`.

```bash
# Install dependencies (first time or after pyproject.toml changes)
uv sync

# Run the CLI
uv run cert-pepper --help

# Database + ingestion (one-time setup)
uv run cert-pepper db init
uv run cert-pepper ingest                           # parses examples/security-plus/ → SQLite
uv run cert-pepper ingest --dry-run                 # parse only, no DB writes

# Study
uv run cert-pepper study                            # adaptive, all domains
uv run cert-pepper study --domain 4 --count 15
uv run cert-pepper progress                         # dashboard: accuracy, predicted score, weak areas
uv run cert-pepper exam                             # 90-question timed mock exam

# AI explanations (requires ANTHROPIC_API_KEY in .env)
uv run cert-pepper pregenerate                      # batch-generate all explanations once

# Tests
uv run pytest                                       # all tests
uv run pytest tests/test_fsrs.py                    # single file
uv run pytest tests/test_fsrs.py::TestStateTransitions::test_new_card_again_enters_learning  # single test

# Lint / type check
uv run ruff check cert_pepper/
uv run mypy cert_pepper/
```

## Architecture

### Data flow
```
examples/security-plus/  (or CONTENT_ROOT)
    └─→ ingestion/ parsers
            └─→ SQLite (cert_pepper.db)
                    ├─→ CLI commands (Typer + Rich TUI)
                    ├─→ MCP servers (3 FastMCP STDIO servers)
                    └─→ AI explainer (Anthropic SDK, cached)
```

### Key modules

**`config.py`** — Pydantic Settings reads `.env`. All path resolution (DB, content root, questions dir, etc.) lives here. `get_settings()` is a factory — call it fresh each time, don't cache the result across module boundaries.

**`db/`** — `connection.py` holds a module-level singleton engine/session factory. `get_session()` is an async context manager that auto-commits or rolls back. `init_db()` reads `schema.sql`, strips `--` comments (to avoid semicolons-in-comments bugs), then executes statements one by one. Always use raw `text()` queries — there are no SQLAlchemy ORM models, only the SQL schema.

**`engine/`** — Pure Python algorithms with no DB dependencies:
- `fsrs.py`: FSRS-4.5 scheduler. `FSRSCard` is a mutable dataclass. Call `schedule(card, rating, now)` → returns a new card. **Difficulty uses a 1–10 scale** (not 0–1); higher = harder. `initial_difficulty(4)` ≈ 3.3 (easy), `initial_difficulty(1)` ≈ 7.2 (hard).
- `bkt.py`: Bayesian Knowledge Tracing. `update(params, is_correct)` → new `BKTParams`. Pure functional — no mutation.
- `selector.py`: Adaptive question selection. Priority: overdue review cards → due learning cards → unseen questions (weighted by domain weight) → least-recently-attempted.
- `scorer.py`: Predicted score = Σ(domain_accuracy × weight) × 900. Pass probability uses logistic sigmoid centered at 750.

**`ingestion/`** — Three parsers for the markdown formats:
- `questions.py`: Splits on `---`, extracts `**QN.**` headers, A/B/C/D options, `<details>` answer blocks. Domain number comes from filename (`domain1-practice.md` → 1).
- `flashcards.py`: Line-by-line scan. `## Section` sets category; `**Term** → Back | Tip` lines become cards.
- `acronyms.py`: Parses `| Acronym | Full Term |` table rows; `## Section` sets category.

**`ai/`** — `client.py` wraps the Anthropic SDK with prompt caching support. `explainer.py` checks the `ai_explanations` DB table before calling the API, then stores the result. For correct answers, it returns the stored markdown explanation directly (no API call). Domain system prompts in `prompts.py` are designed to be ≥1024 tokens for Anthropic cache eligibility.

**`mcp/`** — Three standalone STDIO MCP servers (FastMCP). Each calls `init_db()` at startup. All share the same SQLite file via `DB_PATH` env var. Run with `python -m cert_pepper.mcp.<server_name>`. Registered in `.mcp.json` at the repo root.

**`cli/`** — Typer app in `main.py` imports sub-command modules lazily (inside the command functions) to keep startup fast. Each command is `asyncio.run(...)` of an async function in the corresponding module.

### Database patterns

All queries use SQLAlchemy `text()` with named parameters (`:param`). There are no ORM models. The engine/session are module-level singletons in `connection.py` — the engine is keyed off `DB_PATH` at first call, so tests that need an isolated DB must set `DB_PATH` before any import resolves the singleton.

FSRS card state is stored in `fsrs_cards` with an `ON CONFLICT DO UPDATE` upsert pattern. BKT state is stored in `bkt_skill_states` similarly. The `ai_explanations` table acts as a persistent cache keyed by `(content_type, content_id, explanation_type, selected_answer)`.

### MCP integration

The `.mcp.json` at the repo root registers all three servers. After `uv sync`, server binaries are at `.venv/bin/cert-pepper-*-mcp`. Test a server directly:

```bash
echo '{"jsonrpc":"2.0","id":1,"method":"tools/list"}' | .venv/bin/cert-pepper-study-mcp
```

## Study Content Format

Practice questions follow this exact markdown structure (parsers depend on it):

```markdown
**Q1.** Question stem here?

A) Option A
B) Option B
C) Option C
D) Option D

<details><summary>Answer</summary>

**B) Option B**

Explanation text.

</details>

---
```

Flashcards: `**Term** → Definition | Memory tip` (tip is optional, separated by `|`).
Acronyms: Markdown table rows `| ACRONYM | Full Term |` under `## Category` headers.

Full format documentation: [docs/content-format.md](docs/content-format.md)

## Skills (`.claude/skills/`)

Reusable prompts that keep main-context token usage low. To invoke a skill: read the skill file, perform any required substitutions (e.g. replace `<SHA>` with `$(git rev-parse HEAD)`), then pass the result as the `prompt` to a background Haiku Agent call (`model=haiku`, `run_in_background=true`). The task completion notification signals pass/fail.

| Skill file | Model | When to use |
|---|---|---|
| `ci-watcher.md` | Haiku, background | After every `git push` — **mandatory** |
| `doc-editor/SKILL.md` | (inherits) | Before every `Edit` or `Write` to a `.md` file — **mandatory** |
