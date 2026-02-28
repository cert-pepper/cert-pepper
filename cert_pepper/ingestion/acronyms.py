"""Parse acronyms.md into ParsedAcronym objects."""

from __future__ import annotations

import re
from pathlib import Path

from cert_pepper.models.content import ParsedAcronym

# Matches table rows: | AAA | Authentication, Authorization, Accounting |
_TABLE_ROW = re.compile(r"^\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|")

# Matches ## Section header
_SECTION = re.compile(r"^##\s+(.+)$", re.MULTILINE)

# Skip header/separator rows
_SKIP_ROW = re.compile(r"^[\|\s\-:]+$")


def parse_acronyms(path: Path) -> list[ParsedAcronym]:
    """Parse acronyms.md table format."""
    text = path.read_text(encoding="utf-8")
    acronyms: list[ParsedAcronym] = []

    lines = text.split("\n")
    current_category = "General"

    for line in lines:
        # Check for section header
        sec_match = _SECTION.match(line)
        if sec_match:
            current_category = sec_match.group(1).strip()
            continue

        # Skip separator rows (---|--- etc.)
        if _SKIP_ROW.match(line):
            continue

        # Try to match table row
        row_match = _TABLE_ROW.match(line)
        if not row_match:
            continue

        acronym = row_match.group(1).strip()
        full_term = row_match.group(2).strip()

        # Skip header rows
        if acronym.lower() in ("acronym", "term", "abbreviation"):
            continue
        if not acronym or not full_term:
            continue

        acronyms.append(
            ParsedAcronym(
                acronym=acronym,
                full_term=full_term,
                category=current_category,
            )
        )

    return acronyms
