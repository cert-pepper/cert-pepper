# Content Format Reference

This document describes the markdown format cert-pepper uses for exam content. All three content types (questions, flashcards, acronyms) are plain text files that the ingestion parsers read.

---

## Directory Structure

```
your-exam/
├── practice-questions/
│   ├── domain1-practice.md
│   ├── domain2-practice.md
│   └── domainN-practice.md
├── flashcards/
│   └── key-concepts.md     (any filename works)
└── acronyms.md
```

Set `CONTENT_ROOT=/path/to/your-exam` in `.env`.

---

## Practice Questions

**File naming:** `domainN-practice.md` where `N` is the domain number (1–9). The domain number is extracted from the filename.

**Format:** One question per block, separated by `---`. Each block:

```markdown
**Q1.** Question stem here?

A) Option A
B) Option B
C) Option C
D) Option D

<details><summary>Answer</summary>

**B) Option B**

Explanation text goes here. Can be multiple paragraphs.

The explanation is stored in the DB and shown after incorrect answers.

</details>

---
```

Rules:
- Question header must be `**QN.**` (bold, with period) where N is any integer.
- Options must be `A)`, `B)`, `C)`, `D)` at the start of the line.
- The answer block must use `<details><summary>Answer</summary>`.
- The correct answer line inside details must be `**X) Option text**` (bold).
- Separator `---` must be on its own line between questions.

---

## Flashcards

**File naming:** Any `.md` file under `flashcards/`.

**Format:**

```markdown
## Category Name

**Term** → Definition text | Memory tip (optional)

**Another Term** → Another definition

## Another Category

**Term in new category** → Its definition | Optional tip
```

Rules:
- `## Section` lines set the category for subsequent cards.
- Each card line: `**Term** → Back` or `**Term** → Back | Tip`.
- The `|` separator splits the back text from an optional memory tip.
- Lines not matching this format are ignored.

---

## Acronyms

**File:** `acronyms.md` (must be in CONTENT_ROOT).

**Format:**

```markdown
## Category Name

| Acronym | Full Term |
|---------|-----------|
| AAA | Authentication, Authorization, and Accounting |
| AES | Advanced Encryption Standard |

## Another Category

| Acronym | Full Term |
|---------|-----------|
| PKI | Public Key Infrastructure |
```

Rules:
- `## Section` lines set the category for the acronyms below them.
- Table rows must have exactly two columns: acronym and full term.
- Header rows (`| Acronym | Full Term |`) and separator rows (`|---|---|`) are skipped automatically.

---

## Domain Configuration

The domain numbers in filenames map to domain records in the DB. The ingestion command creates domain records automatically if they don't exist.

If your exam has custom domain names, you can set them up by editing the domain notes structure. The ingestion only cares about the number in the filename for question assignment.

---

## Validation

Test your content before importing:

```bash
uv run cert-pepper ingest --dry-run
```

This parses all files and reports counts without writing to the DB. If counts look wrong, check the file format against the rules above.
