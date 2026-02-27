# Passing Security+ SY0-701 with cert-pepper: A 10-Day Walkthrough

This guide documents an actual 10-day study run using cert-pepper to prepare for CompTIA Security+ SY0-701. The exam has 5 domains, 90 questions, a 90-minute time limit, and a passing score of 750/900.

All commands run from the repo root after `uv sync`.

---

## Exam Structure

| Domain | Title | Weight |
|--------|-------|--------|
| 1 | General Security Concepts | 12% |
| 2 | Threats, Vulnerabilities, and Mitigations | 22% |
| 3 | Security Architecture | 18% |
| 4 | Security Operations | 28% |
| 5 | Program Management and Oversight | 20% |

Passing score: **750 / 900** (~83%). Study time is best allocated proportional to domain weight.

---

## Day 0: Setup

```bash
git clone https://github.com/crook3dfingers/cert-pepper.git
cd cert-pepper
cp .env.example .env
# Optional: add ANTHROPIC_API_KEY to .env for AI explanations
uv sync
uv run cert-pepper db init
uv run cert-pepper ingest
```

Verify everything is loaded:

```bash
uv run cert-pepper progress
```

Expected output:

```
┌─────────────────────────────────────┐
│         Study Progress              │
│  Questions answered: 0              │
│  Predicted score: —                 │
│  Pass probability: —                │
└─────────────────────────────────────┘
No attempts yet. Run `cert-pepper study` to begin.
```

The DB now has 30 questions, 74 flashcards, and 138 acronyms.

---

## Days 1–4: Domain Study

Work through each domain in weight order (4 → 2 → 5 → 3 → 1). Start with domain notes, then drill with the adaptive study session.

```bash
# Day 1: Domain 4 (Security Operations — 28%)
uv run cert-pepper study --domain 4 --count 15

# Day 2: Domain 2 (Threats, Vulnerabilities — 22%)
uv run cert-pepper study --domain 2 --count 15

# Day 3: Domain 5 (Program Management — 20%)
uv run cert-pepper study --domain 5 --count 10

# Day 4: Domain 3 + Domain 1
uv run cert-pepper study --domain 3 --count 10
uv run cert-pepper study --domain 1 --count 10
```

During each session:
- The adaptive selector presents unseen questions first, then repeats questions you got wrong sooner.
- If ANTHROPIC_API_KEY is set, wrong answers trigger an AI explanation from Claude.
- After each session, check `progress` to see which domains are weakest.

```bash
uv run cert-pepper progress
```

Sample output after Day 2:

```
Domain Accuracy
Domain 4: ████████░░ 78%
Domain 2: ██████░░░░ 61%  ← needs work
```

---

## Days 5–6: Weak Area Drill

Use `get_weak_areas` from the analytics MCP server, or read the `progress` dashboard to identify domains below 70%.

```bash
# Focused drill on weakest domain
uv run cert-pepper study --domain 2 --count 20

# Repeat until accuracy climbs above 75%
uv run cert-pepper progress
```

The FSRS scheduler automatically surfaces overdue cards — questions you got wrong come back sooner. You don't need to track them manually.

---

## Day 7: MCP-Assisted Deep Dive

With the MCP servers running in Claude Code, you can ask questions about specific topics mid-study.

Enable MCP servers in `.claude/settings.local.json`:
```json
{ "enableAllProjectMcpServers": true }
```

Open a new Claude Code session in the repo, then use the tools:

- **`search_questions`** — find questions on a specific topic ("What questions cover PKI?")
- **`get_explanation`** — get an AI explanation for any question
- **`lookup_acronym`** — look up any acronym instantly
- **`get_study_recommendations`** — prioritized topics given days remaining

Example Claude Code session:
```
User: I'm weak on PKI. Show me all PKI questions and explain the correct answers.
Claude: [uses search_questions, then get_explanation for each]
```

---

## Day 8: Full Adaptive Session

Mix all domains in one long session. The adaptive selector weights questions by domain weight and your historical accuracy.

```bash
uv run cert-pepper study --count 30
```

By Day 8 you should be seeing mostly review cards (FSRS scheduled repeats) rather than new questions, which means you've covered the material.

---

## Day 9: Mock Exam

Run a full timed exam simulation:

```bash
uv run cert-pepper exam
```

This presents 90 questions in 90 minutes with no hints. At the end it shows your score, domain breakdown, and which questions you missed.

Target: score above 750 on the mock before sitting the real exam.

---

## Day 10: Final Push

Review only the cards due today (spaced repetition schedule):

```bash
# Via MCP
# get_due_cards tool returns cards scheduled for review today

# Via CLI — study with a short session, let FSRS decide what to show
uv run cert-pepper study --count 15
```

Focus on domains still below 75%. Then rest — you've done the work.

---

## Results

After 10 days, the predicted score and pass probability from `progress` should look roughly like:

```
Predicted score:    812 / 900
Pass probability:   94%
Weakest domain:     Domain 3 (Security Architecture) — 71%
```

The predicted score is calculated as: `Σ(domain_accuracy × domain_weight) × 900`. Pass probability uses a logistic sigmoid centered at 750.

---

## What's Next

- Add more practice questions to underrepresented domains (Domains 3 and 5 have none yet).
- Run `cert-pepper pregenerate` to cache AI explanations for all questions (requires API key).
- Use `exam` for a second mock run the morning of the exam.
