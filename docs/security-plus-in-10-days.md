# Security+ in 10 Days

The CertPepper author used this content and schedule to pass Security+ on the first attempt.

CompTIA recommends 40 hours of study for Security+ — 4 hours per day for 10 days. This guide is for candidates with an IT or security background who want a compressed schedule. If you're starting fresh, extend to 3–4 weeks.

CertPepper does not guarantee exam results — outcomes depend on your prior knowledge, study effort, and exam conditions. This sprint uses Claude Code to set up the question bank and generate explanations. The CLI handles studying and practice exams. This is the recommended path.

---

## What a 10-Day Sprint Requires

- **~4 hours/day** — the CompTIA 40-hour benchmark compressed into 10 days
- **2 sessions × 25 questions = 50 questions/day** — roughly 45–60 minutes per session including review time
- **Prior IT/security background** — candidates new to the field should extend to 3–4 weeks

---

## Exam Structure

| Domain | Title | Weight |
|--------|-------|--------|
| 1 | General Security Concepts | 12% |
| 2 | Threats, Vulnerabilities, and Mitigations | 22% |
| 3 | Security Architecture | 18% |
| 4 | Security Operations | 28% |
| 5 | Program Management and Oversight | 20% |

Passing score: **750 / 900** (~83%). Time limit: 90 minutes, 90 questions.

---

## Day 0: Setup

### Primary path — Claude Code with MCP

```bash
# Install uv if needed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Download latest release
curl -L https://github.com/cert-pepper/cert-pepper/archive/refs/tags/v0.6.0.tar.gz | tar xz
cd cert-pepper-0.6.0

# git clone https://github.com/cert-pepper/cert-pepper.git
# cd cert-pepper

cp .env.example .env   # add ANTHROPIC_API_KEY for CLI AI explanations
uv sync
```

Open the repo in Claude Code. MCP servers start automatically (`.mcp.json` is already configured). Then ask Claude to set up your question bank:

```
Set up a question bank for CompTIA Security+ SY0-701
```

Claude sets up the database and confirms when it's ready.

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

For the Security+ example content included in this repo, `CONTENT_ROOT` defaults to `examples/security-plus/`, which loads 228 questions, 135 flashcards, and 262 acronyms.

---

## Days 1–4: Study Sessions

Run two sessions per day. Questions are weighted by domain weight scaled down by your accuracy in that domain — domains where you're weakest get proportionally more questions as your history builds.

```bash
# Morning
uv run cert-pepper study

# Afternoon
uv run cert-pepper study
```

After each PM session, check where you stand:

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

## Day 5: Weak Area Identification

By now you have enough history to spot patterns. Run the AM session as usual, then check your accuracy by domain before the PM session.

**AM session:**

```bash
uv run cert-pepper study
```

**After AM session:**

```bash
uv run cert-pepper progress   # identify domains below 70%
```

**PM session:**

```bash
uv run cert-pepper study
```

---

## Days 6–7: Weak Area Drilling

Both sessions each day. Domains where accuracy is lowest get more questions.

```bash
# Morning
uv run cert-pepper study

# Check again
uv run cert-pepper progress

# Afternoon
uv run cert-pepper study
```

**Day 7 PM — MCP deep dive:** once you've drilled enough questions to know which concepts are sticking, use Claude Code to fill the conceptual gaps:

- "I'm weak on PKI. Show me all PKI questions and explain the correct answers."
- "What acronyms should I know for cryptography?"
- "Explain the difference between IDS and IPS in the context of Security+."
- "Show me every question that covers access control and quiz me on them."

---

## Day 8: Full Adaptive

Both sessions, no domain filter. By this point you'll mostly see review cards — that's expected.

```bash
# Morning
uv run cert-pepper study

# Afternoon
uv run cert-pepper study
```

---

## Day 9: Mock Exam

Run a full timed simulation:

```bash
uv run cert-pepper exam
```

90 questions, 90 minutes, no hints. Target: 750+. Review missed questions afterward — look for patterns across domains rather than re-reading every wrong answer.

---

## Day 10: Due Cards Only

Only cards due for review today appear. No new questions, no cramming.

```bash
uv run cert-pepper study
```

To check whether any questions remain unseen before the exam: `uv run cert-pepper study --new-questions`

Or in Claude Code:

- "Show me my cards due for review today and quiz me on them."
- "Which domains am I still weakest in?"

Then rest.

---

## Results (Illustrative)

The numbers below are made up — they show what the `progress` output format looks like, not what any particular user should expect. Your results depend entirely on your prior knowledge, how many questions you answer, and how you perform.

```
Predicted score:    812 / 900
Pass probability:   94%
Weakest domain:     Domain 3 (Security Architecture) — 71%
```

The predicted score blends your accuracy on seen questions with a 50% prior for unseen ones: `Σ(adjusted_accuracy × domain_weight) × 900`, where `adjusted_accuracy = (raw_accuracy × seen + 0.5 × unseen) / total`. Pass probability uses a logistic sigmoid centered at 750. Neither figure predicts your real exam result.

---

## What's Next

- Run `cert-pepper pregenerate` to pre-cache AI explanations for all wrong-answer combinations (requires `ANTHROPIC_API_KEY`). In Claude Code, explanations are generated on demand — skip `pregenerate`.
- Use `exam` for a second mock run the morning of the exam.
