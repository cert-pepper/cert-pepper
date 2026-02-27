# cert-pepper

> AI-powered adaptive certification prep that learns what you don't know.

Built for Security+ SY0-701 — extensible to any certification.

## Quick Start

```bash
# Install dependencies
cd cert-pepper
uv sync

# Copy and configure environment
cp .env.example .env
# Edit .env with your ANTHROPIC_API_KEY

# Initialize database
uv run cert-pepper db init

# Ingest study content from markdown files
uv run cert-pepper ingest

# Start a study session
uv run cert-pepper study

# Run a mock exam (90 questions)
uv run cert-pepper exam

# View progress dashboard
uv run cert-pepper progress
```

## Commands

| Command | Description |
|---------|-------------|
| `cert-pepper db init` | Create/reset the database |
| `cert-pepper ingest` | Parse markdown content into DB |
| `cert-pepper study [--domain N] [--count N]` | Adaptive study session |
| `cert-pepper quiz --domain N` | Quick quiz on a domain |
| `cert-pepper exam` | 90-question timed mock exam |
| `cert-pepper progress` | Dashboard: accuracy, predicted score, weak areas |
| `cert-pepper pregenerate` | Batch-generate AI explanations |

## Architecture

- **FSRS**: Free Spaced Repetition Scheduler for optimal review timing
- **BKT**: Bayesian Knowledge Tracing for per-topic mastery estimation
- **Adaptive selection**: Prioritizes weak areas and due cards
- **AI explanations**: Pre-generated with Anthropic prompt caching
- **MCP servers**: Usable directly from Claude Code conversations

## MCP Integration

Add to `.claude/settings.json`:

```json
{
  "mcpServers": {
    "cert-pepper-study": {
      "command": "uv",
      "args": ["run", "python", "-m", "cert_pepper.mcp.study_engine"],
      "cwd": "/path/to/cert-pepper"
    },
    "cert-pepper-content": {
      "command": "uv",
      "args": ["run", "python", "-m", "cert_pepper.mcp.content"],
      "cwd": "/path/to/cert-pepper"
    },
    "cert-pepper-analytics": {
      "command": "uv",
      "args": ["run", "python", "-m", "cert_pepper.mcp.analytics"],
      "cwd": "/path/to/cert-pepper"
    }
  }
}
```

## Domain Weights (Security+ SY0-701)

| Domain | Topic | Weight |
|--------|-------|--------|
| 1 | General Security Concepts | 12% |
| 2 | Threats, Vulnerabilities & Mitigations | 22% |
| 3 | Security Architecture | 18% |
| 4 | Security Operations | 28% |
| 5 | Program Management & Oversight | 20% |
