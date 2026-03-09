"""Analytics models: PredictedScore, WeakArea, StudyReport."""

from pydantic import BaseModel


class WeakArea(BaseModel):
    domain_number: int
    domain_name: str
    accuracy_pct: float
    weight_pct: float
    attempts: int
    priority_score: float  # weight × (1 - accuracy) — higher = more urgent


class PredictedScore(BaseModel):
    domain_accuracies: dict[int, float] = {}
    domain_weights: dict[int, float] = {}
    predicted_score: int = 0
    pass_probability: float = 0.0
    coverage_pct: float = 0.0  # fraction of question bank seen (0.0–1.0)

    # Backward-compat shim properties (used by existing MCP / CLI code)
    @property
    def d1_accuracy(self) -> float:
        return self.domain_accuracies.get(1, 0.0)

    @property
    def d2_accuracy(self) -> float:
        return self.domain_accuracies.get(2, 0.0)

    @property
    def d3_accuracy(self) -> float:
        return self.domain_accuracies.get(3, 0.0)

    @property
    def d4_accuracy(self) -> float:
        return self.domain_accuracies.get(4, 0.0)

    @property
    def d5_accuracy(self) -> float:
        return self.domain_accuracies.get(5, 0.0)

    @property
    def weighted_accuracy(self) -> float:
        return sum(
            self.domain_accuracies.get(d, 0.0) * w
            for d, w in self.domain_weights.items()
        )


class StudyRecommendation(BaseModel):
    domain_number: int
    domain_name: str
    reason: str
    urgency: str  # 'critical', 'high', 'medium', 'low'
    suggested_minutes: int


class StudyReport(BaseModel):
    total_questions: int
    total_correct: int
    total_study_minutes: int
    predicted_score: PredictedScore
    weak_areas: list[WeakArea]
    recommendations: list[StudyRecommendation]
    cards_due_today: int
    streak_days: int


class QuestionCounts(BaseModel):
    new: int        # never attempted
    correct: int    # at least one correct attempt
    incorrect: int  # attempted, never correct
    total: int      # all questions for this cert
