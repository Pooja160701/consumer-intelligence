from typing import Any
from app.intelligence.ranking import InsightRanker

class PrioritizationAgent:
    """Assign business priority to a generated insight."""

    def __init__(
        self,
        ranker: InsightRanker | None = None,
    ) -> None:
        self.ranker = ranker or InsightRanker()

    def run(
        self,
        relevance: dict[str, float],
        confidence_score: float,
    ) -> dict[str, Any]:
        relevance_score = relevance.get(
            "overall_score",
            0.0,
        )

        priority_score = (
            relevance_score * 0.70
            + confidence_score * 0.30
        )

        priority_score = round(
            min(priority_score, 1.0),
            4,
        )

        priority = self.ranker.priority_label(
            priority_score
        )

        return {
            "priority_score": priority_score,
            "priority": priority,
        }