"""Parse flashcards/key-concepts.md into ParsedFlashcard objects."""

from __future__ import annotations

import re
from pathlib import Path

from cert_pepper.models.content import ParsedFlashcard


# Matches: ## Section Header
_SECTION = re.compile(r"^##\s+(.+)$", re.MULTILINE)

# Matches flashcard line: **Term** → Definition | Tip
# or **Term** → Definition
_CARD_LINE = re.compile(
    r"^\*\*(.+?)\*\*\s*→\s*(.+?)(?:\s*\|\s*(.+))?$",
    re.MULTILINE,
)


def parse_flashcards(path: Path) -> list[ParsedFlashcard]:
    """Parse flashcards markdown file."""
    text = path.read_text(encoding="utf-8")
    flashcards: list[ParsedFlashcard] = []
    current_category = "General"

    for line in text.split("\n"):
        # Section header (## Category Name)
        sec_match = _SECTION.match(line)
        if sec_match:
            current_category = sec_match.group(1).strip()
            continue

        # Flashcard line (**Term** → Back | Tip)
        card_match = _CARD_LINE.match(line)
        if card_match:
            front = card_match.group(1).strip()
            back = card_match.group(2).strip()
            tip = (card_match.group(3) or "").strip()
            if front and back:
                flashcards.append(
                    ParsedFlashcard(category=current_category, front=front, back=back, tip=tip)
                )

    return flashcards
