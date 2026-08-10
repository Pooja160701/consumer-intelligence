from typing import Any
from app.intelligence.scoring import BrandRelevanceScorer

class BrandContextAgent:
    """Evaluate a signal against the selected brand context."""

    def __init__(
        self,
        scorer: BrandRelevanceScorer | None = None,
    ) -> None:
        self.scorer = scorer or BrandRelevanceScorer()

    def run(
        self,
        signal: dict[str, Any],
        brand: dict[str, Any],
    ) -> dict[str, Any]:
        relevance = self.scorer.score(
            signal,
            brand,
        )

        return {
            "relevance": relevance,
        }