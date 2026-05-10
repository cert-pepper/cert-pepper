# Exam Generation Size Tier Design

## Goal

Prevent undersized generated question banks by making content volume an explicit part of the exam-generation contract.

## Problem

`setup_exam` currently accepts only an exam name. That leaves the content generator without a declared target volume, so it can create a small seed bank while still looking like a complete result. The interface does not force the caller to state whether they want a starter set or a full bank.

## Decision

Add a `size` argument to `setup_exam`. The valid values are:

- `lite`
- `standard`
- `heavy`

If `size` is missing, the tool should default to `standard`. If `size` is invalid, the tool must fail with a structured error that lists the valid options.

## Interface

Change the MCP tool contract from:

- `setup_exam(exam_name, ctx)`

to:

- `setup_exam(exam_name, size=None, ctx)`

Behavior:

- Missing `size` resolves to `standard`.
- Invalid `size` returns an error.
- Existing exam lookup still returns the current `ready` payload, but only after the `size` value has been validated.
- New exam generation uses the resolved `size` tier to choose target content volume.
- The response should include the resolved `size` value so the caller can see what was used.

## Tier Semantics

The size tier should drive deterministic generation targets in code, not only prompt wording.

Tier policy:

- `lite`: at least `20` questions per domain and at least `60` total questions
- `standard`: at least `50` questions per domain and at least `150` total questions
- `heavy`: at least `100` questions per domain and at least `500` total questions

The implementation should define a single mapping from tier name to generation targets. That mapping should include at least:

- per-domain floor
- minimum total questions
- questions per batch
- batches per domain

Allocation rule:

1. Start by assigning the per-domain floor to every domain.
2. Sum those floors to get the floor-based total.
3. If the floor-based total is below the tier minimum total, distribute the remainder across domains by domain weight.
4. If the floor-based total already meets or exceeds the tier minimum total, keep the floor-based plan.

If the product later adds flashcard or acronym generation to `setup_exam`, the same tier mapping should also control those counts.

## Prompting

The question-generation prompt should receive the resolved tier name and the numeric targets it represents. The prompt should not infer size from vague language alone.

That means the MCP server should:

1. validate the requested tier
2. resolve the tier to concrete numeric targets
3. pass the tier label, resolved total, and per-domain targets into sampling prompts

This keeps volume policy in code and leaves the model to generate content within that envelope.

## Testing

Add tests for:

- existing exam with valid size returns `ready`
- missing `size` resolves to `standard`
- invalid `size` is rejected
- each valid tier resolves to the expected generation plan
- weighted remainder allocation behaves as expected when the minimum total exceeds the sum of floors
- generated question numbering still works with the resolved batch plan

The tests should verify behavior at the MCP tool boundary and at any helper that maps size tiers to batch counts.

## Docs

Update user-facing examples that currently say only:

- "Set up a question bank for the CISSP exam"

Those examples should show that the caller must also specify a size tier.

## Non-Goals

This change does not add a new CLI command unless one is needed later. The first fix is to correct the MCP tool contract where generation actually happens.
