# Alabama Permit Content Pack Design

## Goal

Add a new CertPepper content pack for the Alabama driver's permit test. The pack will support study notes, flashcards, and practice exams for the permit exam content used statewide in Alabama. Madison County does not require a separate content model, so the pack will focus on Alabama handbook material rather than county-specific logistics.

## Scope

This work creates a self-contained content directory under `examples/` using the repository's existing markdown formats.

Included:

- study material organized by permit-test topic
- flashcards for recall practice
- practice questions grouped by topic
- at least one mixed practice exam set for timed review
- exam metadata in `exam.yaml`

Excluded:

- CLI changes
- database schema changes
- adaptive engine changes
- county office logistics beyond a brief mention in the README, if needed

## Content Structure

Use a new directory such as `examples/alabama-permit/` with the same shape as the Security+ reference pack:

- `exam.yaml`
- `README.md`
- `study-plan.md`
- `acronyms.md`
- `flashcards/`
- `practice-questions/`

The questions parser expects filenames of the form `domainN-practice.md`, so the Alabama pack should follow that convention.

## Proposed Domains

The permit content should be split into topic areas that match the Alabama driver manual and permit exam expectations:

1. Traffic signs, signals, and pavement markings
2. Rules of the road and right-of-way
3. Safe driving practices and speed control
4. Sharing the road, parking, turns, and lane usage
5. Alcohol, drugs, penalties, and crash response
6. Permit eligibility, licensing basics, and driver responsibilities

These domains are chosen to keep the content readable and to support adaptive study sessions with meaningful topic-level coverage.

## Study Experience

The study plan should provide a short path for a first-time learner:

- read the topic notes once
- drill the flashcards
- answer questions by domain
- finish with a mixed practice exam

The README should explain how to ingest the pack and how to use it with the existing `cert-pepper` commands.

## Validation

Before considering the pack complete:

- `cert-pepper ingest --dry-run` should parse the new content without errors
- the pack should include non-empty study, flashcard, and question content
- the practice question format should match the repository's existing parser rules
- `exam.yaml` should parse and expose a sane domain layout for the Alabama permit test

## Notes

The Alabama permit test is a state-level exam, so Madison County should not change the core study material. If a future update adds office-specific details, that should live in a separate reference note rather than in the study bank itself.
