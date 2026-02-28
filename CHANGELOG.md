# Changelog

## [0.1.0] — 2026-02-27

### Added
- Adaptive CLI study loop (FSRS-4.5 spaced repetition + BKT mastery tracking)
- 90-question timed mock exam mode
- Progress dashboard: domain accuracy, predicted score, pass probability
- AI explanations via Anthropic API (CLI) and MCP sampling (no API key needed)
- Batch pre-generation of AI explanations (`pregenerate` command)
- Three FastMCP STDIO servers: study-engine, content, analytics
- `setup_exam` MCP tool: generates a full question bank for any exam via MCP sampling
- Multi-exam support: certifications + domains schema, cert-scoped scoring
- Security+ SY0-701 example content: 160 practice questions (domains 1, 2, 4),
  74 flashcards, 138 acronyms
- Content ingestion pipeline for markdown question/flashcard/acronym format
- `content-format.md` spec for authoring exam content
- 10-day Security+ walkthrough guide
