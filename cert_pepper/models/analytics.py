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
    d1_accuracy: float = 0.0
    d2_accuracy: float = 0.0
    d3_accuracy: float = 0.0
    d4_accuracy: float = 0.0
    d5_accuracy: float = 0.0
    predicted_score: int = 0
    pass_probability: float = 0.0

    @property
    def weighted_accuracy(self) -> float:
        weights = [0.12, 0.22, 0.18, 0.28, 0.20]
        accuracies = [
            self.d1_accuracy,
            self.d2_accuracy,
            self.d3_accuracy,
            self.d4_accuracy,
            self.d5_accuracy,
        ]
        return sum(w * a for w, a in zip(weights, accuracies))


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
