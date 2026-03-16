# Contributing to CertPepper

Thanks for your interest in contributing. This guide covers setup, workflow, and conventions.

## Prerequisites

- Python 3.12+
- [uv](https://astral.sh/uv) package manager

## Dev Setup

```bash
git clone https://github.com/cert-pepper/cert-pepper.git
cd cert-pepper
cp .env.example .env
uv sync
uv run cert-pepper db init
uv run cert-pepper ingest
```

This creates a working database with the bundled Security+ example content.

## TDD Red-Green Workflow

All code changes follow test-driven development:

1. **Write a failing test** — run it, confirm it fails with the expected error.
2. **Write the minimal code** to make the test pass.
3. **Refactor** if needed, keeping tests green.

Do not write production code without a corresponding test. See `CLAUDE.md` for test patterns and fixtures.

## Running Checks

```bash
uv run pytest                        # full test suite
uv run ruff check cert_pepper/       # lint
uv run mypy cert_pepper/             # type check
```

## Pull Request Checklist

Before opening a PR, verify:

- [ ] `uv run pytest` passes
- [ ] `uv run ruff check cert_pepper/` is clean
- [ ] `uv run mypy cert_pepper/` is clean
- [ ] `CHANGELOG.md` updated (if the change is user-facing)
- [ ] New tests cover the change

## Content Authoring

If you're adding practice questions or flashcards:

- Follow the format spec in [docs/content-format.md](docs/content-format.md)
- Never expand acronyms in answer options — use the bare acronym (e.g. `SOAR`, not `SOAR — Security Orchestration, Automation, and Response`)
- Place content under `examples/<exam-name>/`

## Reporting Security Issues

Do not use public issues for security vulnerabilities. See [SECURITY.md](SECURITY.md) for reporting instructions.
