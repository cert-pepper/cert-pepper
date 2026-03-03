# Passing Security+ SY0-701 with cert-pepper: A 10-Day Walkthrough

This guide documents an actual 10-day study run using cert-pepper to prepare for CompTIA Security+ SY0-701. The exam has 5 domains, 90 questions, a 90-minute time limit, and a passing score of 750/900.

This walkthrough assumes you're using **Claude Code with MCP enabled** — that's the recommended path. A manual CLI alternative is noted where it differs.

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

### Primary path — Claude Code with MCP

```bash
git clone https://github.com/crook3dfingers/cert-pepper.git
cd cert-pepper
uv sync
```

Open the repo in Claude Code. MCP servers start automatically (`.mcp.json` is already configured). Then ask Claude to set up your question bank:

```
Set up a question bank for CompTIA Security+ SY0-701
```

Claude calls `setup_exam` behind the scenes, initialises the database, and confirms when it's ready. No manual `db init` or `ingest` step needed.

Verify everything loaded:

```
Show me my study progress
```

Expected reply: 0 questions answered, no predicted score yet — that's correct.

### Alternative path — manual CLI

Use this if you're not running Claude Code or want to bring your own exam content:

```bash
cp .env.example .env
# Set CONTENT_ROOT in .env to point at your exam content directory
uv run cert-pepper db init
uv run cert-pepper ingest   # ingests whatever CONTENT_ROOT points to
```

For the Security+ example content included in this repo, `CONTENT_ROOT` defaults to `examples/security-plus/`, which loads 160 questions, 74 flashcards, and 138 acronyms.

---

## Days 1–4: Domain Study

Run a study session each day — no flags needed. The adaptive selector already knows which domains need the most work:

```bash
uv run cert-pepper study
```

The selector weights questions by domain weight and your historical accuracy, so high-weight domains (Security Operations at 28%, Threats at 22%) surface more often automatically. You don't need to manually schedule by domain.

During each session:
- Unseen questions appear first; questions you got wrong come back sooner (FSRS scheduling).
- Wrong answers trigger an AI explanation from Claude. When using Claude Code with MCP, explanations work without an API key.
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

With MCP enabled in Claude Code, you can do a natural-language deep dive on any topic. Just ask — no tool names needed. Example prompts:

- "I'm weak on PKI. Show me all PKI questions and explain the correct answers."
- "What acronyms should I know for cryptography?"
- "I have 3 days until the exam. What should I focus on?"
- "Explain the difference between IDS and IPS in the context of Security+."
- "Show me every question that covers access control and quiz me on them."

Claude uses the search, explanation, acronym, and analytics tools behind the scenes.

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

Review only the cards due today. In Claude Code:

- "Show me my cards due for review today and quiz me on them."
- "Which domains am I still weakest in?"
- "Give me 10 quick-fire questions on my worst domain."

Via CLI:

```bash
uv run cert-pepper study --count 15
```

FSRS decides what to show — it will surface overdue cards first.

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
- Run `cert-pepper pregenerate` to pre-cache AI explanations for all wrong-answer combinations (requires `ANTHROPIC_API_KEY`). Skip this if you're using Claude Code — the `get_explanation` MCP tool generates explanations on demand without an API key.
- Use `exam` for a second mock run the morning of the exam.
