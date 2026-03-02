# cert-pepper

AI-powered adaptive certification prep. Learns what you don't know.

cert-pepper ingests your exam content (questions, flashcards, acronyms) into SQLite and runs an adaptive study loop using **FSRS-4.5 spaced repetition** and **Bayesian Knowledge Tracing**. Wrong answers get AI explanations from Claude. Three MCP servers expose the study engine, content, and analytics to Claude Code.

**Worked example:** [Passing Security+ SY0-701 in 10 days](docs/walkthrough.md)

---

## Quick Start

```bash
# Install uv (skip if already installed — https://astral.sh/uv)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Option 1: download the latest release
curl -L https://github.com/crook3dfingers/cert-pepper/archive/refs/tags/v0.2.0.tar.gz | tar xz
cd cert-pepper-0.2.0

# Option 2: clone (to track future updates)
# git clone https://github.com/crook3dfingers/cert-pepper.git
# cd cert-pepper

cp .env.example .env          # add ANTHROPIC_API_KEY for AI explanations in CLI study sessions
uv sync
```

Open the repo in **Claude Code** (see [MCP Integration](#mcp-integration) to enable the servers). Ask Claude to build a question bank for your exam:

> Set up a question bank for the CISSP exam

Claude runs `setup_exam`, generates ~90 AI-written practice questions per domain, and loads them into the database. Then start studying:

```bash
uv run cert-pepper study
```

To use hand-crafted markdown content instead, see [Adding Your Own Exam](#adding-your-own-exam).

---

## CLI Reference

| Command | Description |
|---------|-------------|
| `cert-pepper db init` | Create the SQLite schema |
| `cert-pepper ingest [--dry-run]` | Parse markdown content into the DB |
| `cert-pepper study [--domain N] [--count N]` | Adaptive study session |
| `cert-pepper exam` | 90-question timed mock exam |
| `cert-pepper progress` | Dashboard: accuracy, predicted score, weak areas |
| `cert-pepper pregenerate` | Batch-generate AI explanations (requires API key) |

---

## MCP Integration

Three STDIO MCP servers are registered in `.mcp.json`. After `uv sync` they are available as venv binaries:

| Server | Binary | Purpose |
|--------|--------|---------|
| `cert-pepper-study` | `.venv/bin/cert-pepper-study-mcp` | Start sessions, submit answers, get due cards |
| `cert-pepper-content` | `.venv/bin/cert-pepper-content-mcp` | Search questions, get explanations, look up acronyms |
| `cert-pepper-analytics` | `.venv/bin/cert-pepper-analytics-mcp` | Predict score, find weak areas, study recommendations |

Enable them in Claude Code by adding `enableAllProjectMcpServers: true` to `.claude/settings.local.json`, then open a new session in this repo.

The `get_explanation` MCP tool generates AI explanations via MCP sampling — no `ANTHROPIC_API_KEY` required when using Claude Code.

Test a server directly:
```bash
echo '{"jsonrpc":"2.0","id":1,"method":"tools/list"}' | .venv/bin/cert-pepper-study-mcp
```

---

## Adding Your Own Exam

1. Create a content directory with your exam material in the cert-pepper markdown format (see [docs/content-format.md](docs/content-format.md)).
2. Set `CONTENT_ROOT=/path/to/your/content` in `.env`.
3. Run `cert-pepper db init` and `cert-pepper ingest`.

The Security+ content in `examples/security-plus/` is a complete reference implementation.

---

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `DB_PATH` | `./cert_pepper.db` | SQLite database path |
| `CONTENT_ROOT` | `./examples/security-plus` | Root of your exam content |
| `ANTHROPIC_API_KEY` | — | Required for CLI AI explanations (`study`, `pregenerate`). Not needed when using MCP tools from Claude Code. |
| `HAIKU_MODEL` | `claude-haiku-4-5-20251001` | Model for AI explanations |
| `SONNET_MODEL` | `claude-sonnet-4-6` | Model for MCP sampling |
| `DEFAULT_SESSION_SIZE` | `10` | Questions per study session |
| `MASTERY_THRESHOLD` | `0.85` | BKT mastery cutoff |

---

## Repository Layout

```
cert-pepper/
├── cert_pepper/          — Python source (CLI, MCP servers, algorithms)
│   ├── cli/              — Typer commands
│   ├── mcp/              — Three FastMCP STDIO servers
│   ├── engine/           — FSRS, BKT, selector, scorer (pure Python)
│   ├── ingestion/        — Markdown parsers
│   ├── ai/               — Anthropic client + explainer
│   └── db/               — SQLAlchemy async engine + schema
├── tests/                — pytest suite (197 tests)
├── examples/
│   └── security-plus/    — Security+ SY0-701 exam content
└── docs/
    ├── walkthrough.md    — 10-day Security+ study guide
    └── content-format.md — Format spec for your own exam content
```

---

## Worked Example

The `examples/security-plus/` directory contains a complete Security+ SY0-701 exam prep set:

- 5 domains of notes
- 74 flashcards
- 30 practice questions across 3 domains
- 138 acronyms

See [docs/walkthrough.md](docs/walkthrough.md) for a step-by-step guide showing how to use cert-pepper to prepare for Security+ in 10 days.
