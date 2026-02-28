"""Content models: Question, Flashcard, Acronym, Domain, ExamConfig."""

from pydantic import BaseModel


class ExamDomain(BaseModel):
    """A domain entry in exam.yaml."""

    number: int
    name: str
    weight_pct: float


class ExamConfig(BaseModel):
    """Top-level exam.yaml model."""

    code: str
    name: str
    vendor: str = ""
    passing_score: int = 750
    max_score: int = 900
    domains: list[ExamDomain]


class Domain(BaseModel):
    id: int
    number: int
    name: str
    weight_pct: float


class Question(BaseModel):
    id: int
    domain_id: int
    domain_number: int = 0
    number: int
    stem: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    correct_answer: str  # 'A', 'B', 'C', 'D'
    explanation: str = ""
    difficulty: float = 0.3
    source_file: str = ""

    def get_option(self, letter: str) -> str:
        return {
            "A": self.option_a,
            "B": self.option_b,
            "C": self.option_c,
            "D": self.option_d,
        }[letter.upper()]

    def options_dict(self) -> dict[str, str]:
        return {
            "A": self.option_a,
            "B": self.option_b,
            "C": self.option_c,
            "D": self.option_d,
        }


class Flashcard(BaseModel):
    id: int
    domain_id: int | None
    category: str
    front: str
    back: str
    tip: str = ""


class Acronym(BaseModel):
    id: int
    acronym: str
    full_term: str
    category: str = ""


class ParsedQuestion(BaseModel):
    """Intermediate model during parsing — no ID yet."""
    domain_number: int
    number: int
    stem: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    correct_answer: str
    explanation: str = ""
    source_file: str = ""


class ParsedFlashcard(BaseModel):
    """Intermediate model during parsing."""
    category: str
    front: str
    back: str
    tip: str = ""


class ParsedAcronym(BaseModel):
    """Intermediate model during parsing."""
    acronym: str
    full_term: str
    category: str = ""
