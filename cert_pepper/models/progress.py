"""Progress models: FSRSCard, BKTState, Attempt, Session."""

from datetime import datetime
from enum import IntEnum

from pydantic import BaseModel


class FSRSRating(IntEnum):
    AGAIN = 1
    HARD = 2
    GOOD = 3
    EASY = 4


class FSRSState(str):
    NEW = "new"
    LEARNING = "learning"
    REVIEW = "review"
    RELEARNING = "relearning"


class FSRSCard(BaseModel):
    id: int
    user_id: int
    content_type: str  # 'question' or 'flashcard'
    content_id: int
    stability: float = 1.0
    difficulty: float = 0.3
    retrievability: float = 1.0
    due_date: datetime
    last_review: datetime | None = None
    state: str = "new"
    step: int = 0
    reps: int = 0
    lapses: int = 0


class BKTState(BaseModel):
    id: int
    user_id: int
    skill_id: int
    skill_type: str  # 'domain' or 'topic'
    p_mastery: float = 0.1
    p_learn: float = 0.3
    p_guess: float = 0.2
    p_slip: float = 0.1
    attempts: int = 0
    correct: int = 0
    theta: float = 0.0
    accuracy_pct: float = 0.0


class QuestionAttempt(BaseModel):
    id: int | None = None
    session_id: int
    user_id: int
    question_id: int
    selected_answer: str
    is_correct: bool
    time_taken_seconds: float = 0.0
    confidence_rating: int | None = None
    hint_used: bool = False


class StudySession(BaseModel):
    id: int | None = None
    user_id: int
    session_type: str  # 'study', 'quiz', 'exam', 'flashcard'
    domain_filter: int | None = None
    started_at: datetime | None = None
    ended_at: datetime | None = None
    questions_seen: int = 0
    questions_correct: int = 0
    total_time_seconds: int = 0

    @property
    def accuracy(self) -> float:
        if self.questions_seen == 0:
            return 0.0
        return self.questions_correct / self.questions_seen
