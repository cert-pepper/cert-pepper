# Multi-Exam Study Selection Design

## Problem

`cert-pepper study` currently delegates exam resolution to a shared helper that raises when more than one exam exists in the database and the user did not pass `--exam`. That produces a low-value error for new users.

The same resolver is also used by the MCP study server. In MCP mode, the current behavior is also an opaque error instead of a structured prompt that lets the caller choose from the available exams.

## Goals

- Make `cert-pepper study` usable without `--exam` when multiple exams exist.
- Provide an interactive selector in CLI TTY sessions.
- Preserve a clear fallback for non-interactive CLI environments.
- Return a structured selection request from MCP instead of a generic error.
- Keep exam discovery and matching logic shared so CLI and MCP stay consistent.

## Non-Goals

- Changing the quiz, exam, progress, or goal commands in this iteration.
- Adding fuzzy ranking beyond partial substring matching on code and exam name.
- Introducing persistent user preferences for a default exam.

## User Experience

### CLI

When `study` is invoked with `--exam`, behavior remains unchanged: resolve that exact exam code or fail clearly if it does not exist.

When `study` is invoked without `--exam`:

- If zero exams exist, return the existing "run ingest first" style error.
- If one exam exists, auto-select it.
- If multiple exams exist and stdout/stdin is attached to a TTY:
  - If exam count is `<= 8`, show all exams in an interactive arrow-key menu.
  - If exam count is `> 8`, show a shorter menu containing the first few exams plus an `Other...` option.
  - Choosing `Other...` prompts the user to type part of an exam code or exam name.
  - Partial matching is case-insensitive and checks both exam code and exam name.
  - If the typed query returns one match, select it immediately.
  - If the typed query returns multiple matches, show an interactive narrowed chooser.
  - If the typed query returns zero matches, show a retry message and prompt again.
- If multiple exams exist and the CLI is not interactive, print a clear error that explains `--exam` is required in non-interactive mode and includes a short list of available exam codes.

### MCP

When `start_session` is invoked with `exam_code`, behavior remains unchanged: exact-code lookup or clear not-found error.

When `start_session` is invoked without `exam_code`:

- If zero exams exist, return the existing no-exams error.
- If one exam exists, auto-select it.
- If multiple exams exist, return structured JSON with:
  - `status: "selection_required"`
  - a user-facing `message`
  - an `options` array with exam codes and names
  - a note that the caller can retry with `exam_code`

For large exam sets, MCP still returns the full option set because the caller is expected to render or filter it. Truncation is unnecessary there and would make the contract less useful.

## Shared Resolution Model

The existing `resolve_cert_id(session, exam_code)` helper should stop being the only interface for multi-exam flows. Instead, the code should introduce a shared discovery/resolution layer that can represent three states:

- resolved
- not found / no exams
- selection required

A small structured model is preferable to plain exceptions for the normal "multiple choices available" path.

Suggested shape:

- `ExamChoice`: `id`, `code`, `name`
- `ExamResolutionResult`:
  - `status`: `resolved` or `selection_required`
  - `cert_id`: present when resolved
  - `options`: present when selection is required

The exact class/form can be dataclass, Pydantic model, or dict-oriented helper, but the behavior must be centralized in one place.

## Matching Rules

- Exact code lookup remains the behavior when `exam_code` is explicitly provided.
- The `Other...` path uses case-insensitive partial substring matching against:
  - certification code
  - certification name
- Match outcomes:
  - one match: use it
  - multiple matches: prompt again with a narrowed chooser
  - zero matches: show retry guidance

This keeps the explicit `--exam` contract strict while making interactive discovery forgiving.

## CLI Menu Design

The CLI currently uses Rich prompts but has no reusable selector widget. This change should add a small exam-selection helper in the CLI layer rather than embedding ad hoc prompting in `run_study_session`.

Behavior requirements:

- Detect TTY before attempting arrow-key interaction.
- Support arrow-key selection in TTY mode.
- Provide a numbered/text fallback for non-TTY sessions.
- Keep the helper focused on choosing an exam, not generic menu abstraction.

Dependency choice is an implementation detail, but the selector must work reliably in local terminal sessions and degrade cleanly when interactive capabilities are unavailable.

## MCP Contract

`start_session(...)` should no longer return a plain error when multiple exams exist and no `exam_code` was provided. Instead it should return a JSON payload the MCP client can use to ask the user which exam they want.

Suggested response:

```json
{
  "status": "selection_required",
  "message": "Multiple exams found. Choose one and retry with exam_code.",
  "options": [
    {"code": "SY0-701", "name": "CompTIA Security+"},
    {"code": "AL-PERMIT", "name": "Alabama Driver Permit Test"}
  ]
}
```

This is a normal interaction state, not an internal error.

## Files Likely Affected

- `cert_pepper/db/exams.py`
- `cert_pepper/cli/study.py`
- `cert_pepper/mcp/study_engine.py`
- `tests/test_study.py`
- `tests/test_mcp_study_engine.py`
- new tests for resolver behavior

`cert_pepper/cli/main.py` likely stays unchanged because it already passes `exam` through to `run_study_session`.

## Testing Strategy

Test-first coverage should include:

- resolver returns the single exam automatically
- resolver returns selection-required when multiple exams exist and no code is provided
- exact code lookup still works
- explicit invalid code still fails clearly
- CLI interactive path selects an exam and starts the session
- CLI large-list path exposes `Other...`
- CLI `Other...` query:
  - one match
  - multiple matches
  - zero matches and retry
- CLI non-interactive path fails with actionable guidance
- MCP `start_session` returns `selection_required` payload when multiple exams exist
- MCP `start_session` still starts normally when one exam exists or when `exam_code` is explicit

## Risks

- Terminal interactivity can be brittle if the selector dependency behaves differently across environments.
- Mixing exact-code resolution and partial interactive matching could create ambiguity if the boundaries are not explicit.
- If the interactive exam-selection helper is too generic, it may become harder to test than necessary.

## Recommended Implementation Direction

Use a centralized resolution/discovery helper that returns structured outcomes, then adapt the final user interaction per surface:

- CLI TTY: interactive chooser
- CLI non-TTY: actionable error
- MCP: structured `selection_required` response

This keeps the exam-selection rules in one place while letting each interface present the choice appropriately.
