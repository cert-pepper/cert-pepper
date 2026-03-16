# Changelog

All notable changes to CertPepper are documented here.

## [0.5.4] — 2026-03-08

### Added
- Live countdown timer in exam mode with automatic expiry
- Exam mode prefers unseen questions with freshness summary

### Fixed
- "Mastered" label suppressed in domain performance until 50% coverage reached

## [0.5.3] — 2026-03-07

### Added
- Coverage-adjusted score prediction with 50% prior for unseen questions

### Fixed
- `--new-questions` mode returns `None` when no unseen questions remain
- Ruff line-too-long violations in `main.py`

## [0.5.2] — 2026-03-06

### Added
- `--new-questions` flag for `study` command to focus on unseen material

## [0.5.1] — 2026-03-05

### Added
- Acronym-expansion rule enforced in generated questions
- CI-watcher skill: self-obtains commit SHA and fetches failure logs

### Fixed
- API errors surfaced in ci-watcher instead of silently swallowed
- Mypy type errors in `goals.py` and `goal.py`
- Release skill creates GitHub Release via `gh release create`

## [0.5.0] — 2026-03-04

### Added
- Accuracy-weighted unseen question selection
- Adaptive study schedule with calendar tracking
- Study streak tracking on the progress dashboard
- CI-watcher skill for post-push CI monitoring
- Doc-editor skill for markdown review
- Default session size raised to 25 questions

### Changed
- Walkthrough rewritten as a 10-day adaptive sprint

## [0.4.0] — 2026-03-02

### Added
- Dynamic versioning via hatch-vcs
- `/release` skill for tagging and publishing releases

## [0.3.0] — 2026-03-01

### Added
- `cert-pepper upgrade` command

### Fixed
- Stratified per-domain sampling in unseen question selector

## [0.2.0] — 2026-02-28

### Added
- `setup_exam` MCP tool enriched with Reddit community research

### Changed
- Quick Start rewritten to use MCP `setup_exam` as the primary onboarding path

## [0.1.0] — 2026-02-27

### Added
- Adaptive CLI study loop (FSRS-4.5 spaced repetition + BKT mastery tracking)
- 90-question timed mock exam mode
- Progress dashboard: domain accuracy, predicted score, pass probability
- AI explanations via Anthropic API (CLI) and MCP sampling
- Batch pre-generation of AI explanations (`pregenerate` command)
- Three FastMCP STDIO servers: study-engine, content, analytics
- `setup_exam` MCP tool: generates a full question bank for any exam via MCP sampling
- Multi-exam support: certifications and domains schema, cert-scoped scoring
- Security+ SY0-701 example content: 160 practice questions, 74 flashcards, 138 acronyms
- Content ingestion pipeline for markdown question/flashcard/acronym format
- `content-format.md` spec for authoring exam content
- 10-day Security+ walkthrough guide
