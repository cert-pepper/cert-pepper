# Agent Instructions

## Question Bank Requests

When a user asks to set up, create, or generate a question bank for an exam, treat that as a request to use the MCP content server's exam-generation workflow.

Primary tool:

- `create_question_bank(exam_name, size=None, ctx=None)`

Equivalent lower-level tool:

- `setup_exam(exam_name, size=None, ctx=None)`

Rules:

- Prefer `create_question_bank` because its name matches the user-facing request.
- Use `size="lite"`, `"standard"`, or `"heavy"` when the user specifies a tier. If omitted, default behavior is `standard`.
- This workflow creates or reuses a DB-backed question bank. It does not create files under `examples/`.
- Do not scaffold a new local content pack unless the user explicitly asks for authored markdown content in the repository.
- If the exam already exists, return the ready status from the MCP tool instead of regenerating content.
