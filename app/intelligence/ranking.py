from typing import Any

class InsightRanker:
    """Rank brand-signal opportunities."""

    def rank(
        self,
        scored_items: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        """Return items ordered by descending priority score."""

        return sorted(
            scored_items,
            key=lambda item: (
                item.get(
                    "priority_score",
                    0.0,
                ),
                item.get(
                    "relevance_score",
                    0.0,
                ),
            ),
            reverse=True,
        )

    @staticmethod
    def priority_label(
        priority_score: float,
    ) -> str:
        """Convert numeric priority into a business label."""

        if priority_score >= 0.80:
            return "P1"

        if priority_score >= 0.60:
            return "P2"

        if priority_score >= 0.40:
            return "P3"

        return "P4"