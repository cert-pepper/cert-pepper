"""Parse practice-questions/domain*.md files into structured Question objects."""

from __future__ import annotations

import re
from pathlib import Path

from cert_pepper.models.content import ParsedQuestion

# Matches: **Q1.** or **Q1)**
_Q_HEADER = re.compile(r"\*\*Q(\d+)[.)]\*\*\s*(.*?)(?=\n)", re.DOTALL)

# Matches option lines: "A) Some text" or "A. Some text"
_OPTION = re.compile(r"^([A-D])[).]\s+(.+)$", re.MULTILINE)

# Matches answer inside <details> block: **B) DDoS** or **B. DDoS**
_ANSWER = re.compile(
    r"<details><summary>Answer</summary>\s*\*\*([A-D])[).][^*]*\*\*\s*(.*?)\s*</details>",
    re.DOTALL,
)

# Extract domain number from filename: domain1-practice.md → 1
_DOMAIN_NUM = re.compile(r"domain(\d+)", re.IGNORECASE)


def _parse_questions_content(
    content: str, domain_number: int, source_file: str
) -> list[ParsedQuestion]:
    """Parse question markdown content into ParsedQuestion list."""
    questions: list[ParsedQuestion] = []

    # Split on horizontal rules to get question blocks
    blocks = re.split(r"\n---\n", content)

    for block in blocks:
        block = block.strip()
        if not block:
            continue

        # Must have a question header
        q_match = _Q_HEADER.search(block)
        if not q_match:
            continue

        q_number = int(q_match.group(1))
        stem = q_match.group(2).strip()

        # If stem is empty or cut off, grab next line(s)
        if not stem:
            after = block[q_match.end():]
            stem_lines = []
            for line in after.split("\n"):
                line = line.strip()
                if not line or _OPTION.match(line):
                    break
                stem_lines.append(line)
            stem = " ".join(stem_lines).strip()

        # Parse options
        options: dict[str, str] = {}
        for opt_match in _OPTION.finditer(block):
            letter = opt_match.group(1).upper()
            text_val = opt_match.group(2).strip()
            options[letter] = text_val

        if len(options) < 4:
            # Try alternate parsing — look for A) through D) anywhere in block
            for line in block.split("\n"):
                line = line.strip()
                m2 = re.match(r"^([A-D])[).]\s+(.+)$", line)
                if m2:
                    options[m2.group(1).upper()] = m2.group(2).strip()

        if len(options) < 4:
            continue  # skip malformed question

        # Parse answer + explanation
        ans_match = _ANSWER.search(block)
        correct_answer = ""
        explanation = ""
        if ans_match:
            correct_answer = ans_match.group(1).upper()
            explanation = ans_match.group(2).strip()
            # Clean up: remove leading answer line if repeated
            exp_lines = explanation.split("\n")
            if exp_lines:
                # Remove empty first line
                while exp_lines and not exp_lines[0].strip():
                    exp_lines.pop(0)
            explanation = "\n".join(exp_lines).strip()

        if not correct_answer or correct_answer not in "ABCD":
            continue

        questions.append(
            ParsedQuestion(
                domain_number=domain_number,
                number=q_number,
                stem=stem,
                option_a=options.get("A", ""),
                option_b=options.get("B", ""),
                option_c=options.get("C", ""),
                option_d=options.get("D", ""),
                correct_answer=correct_answer,
                explanation=explanation,
                source_file=source_file,
            )
        )

    return questions


def parse_questions_file(path: Path) -> list[ParsedQuestion]:
    """Parse a single domain practice file and return ParsedQuestion list."""
    content = path.read_text(encoding="utf-8")
    filename = path.name

    # Get domain number from filename
    m = _DOMAIN_NUM.search(filename)
    if not m:
        raise ValueError(f"Cannot determine domain number from filename: {filename}")
    domain_number = int(m.group(1))

    return _parse_questions_content(content, domain_number, filename)


def parse_questions_text(text: str, domain_number: int) -> list[ParsedQuestion]:
    """Parse question markdown text (not a file) and return ParsedQuestion list.

    Unlike parse_questions_file(), the domain_number is supplied explicitly
    (there is no filename to derive it from). source_file is set to "generated".
    """
    return _parse_questions_content(text, domain_number, "generated")


def parse_all_questions(questions_dir: Path) -> list[ParsedQuestion]:
    """Parse all domain*.md files in the questions directory."""
    all_questions: list[ParsedQuestion] = []
    files = sorted(questions_dir.glob("domain*-practice.md"))

    for f in files:
        parsed = parse_questions_file(f)
        all_questions.extend(parsed)

    return all_questions
