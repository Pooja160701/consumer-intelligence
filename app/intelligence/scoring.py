from typing import Any

class BrandRelevanceScorer:
    """
    Calculate how relevant a signal is to a brand.

    The score combines:
    - category alignment
    - keyword overlap
    - strategic priority alignment
    - target consumer alignment
    - geography alignment
    """

    def score(
        self,
        signal: dict[str, Any],
        brand: dict[str, Any],
    ) -> dict[str, float]:
        """Return detailed relevance scores."""

        signal_text = self._signal_text(signal)

        category_score = self._category_score(
            signal,
            brand,
        )

        keyword_score = self._keyword_score(
            signal_text,
            brand,
        )

        strategic_score = self._strategic_score(
            signal_text,
            brand,
        )

        consumer_score = self._consumer_score(
            signal_text,
            brand,
        )

        geography_score = self._geography_score(
            signal,
            brand,
        )

        overall_score = (
            category_score * 0.30
            + keyword_score * 0.30
            + strategic_score * 0.20
            + consumer_score * 0.10
            + geography_score * 0.10
        )

        return {
            "category_score": round(
                category_score,
                4,
            ),
            "keyword_score": round(
                keyword_score,
                4,
            ),
            "strategic_score": round(
                strategic_score,
                4,
            ),
            "consumer_score": round(
                consumer_score,
                4,
            ),
            "geography_score": round(
                geography_score,
                4,
            ),
            "overall_score": round(
                min(overall_score, 1.0),
                4,
            ),
        }

    @staticmethod
    def _signal_text(
        signal: dict[str, Any],
    ) -> str:
        """Create searchable signal text."""

        return " ".join(
            [
                str(signal.get("title", "")),
                str(signal.get("text", "")),
                str(signal.get("category", "")),
                str(signal.get("signal_type", "")),
            ]
        ).lower()

    @staticmethod
    def _category_score(
        signal: dict[str, Any],
        brand: dict[str, Any],
    ) -> float:
        """Score category alignment."""

        signal_category = str(
            signal.get("category", "")
        ).lower()

        brand_category = str(
            brand.get("category", "")
        ).lower()

        if not signal_category or not brand_category:
            return 0.0

        if signal_category == brand_category:
            return 1.0

        # Handle useful semantic category relationships.
        related_categories = {
            "healthy_snacks": {
                "snacks",
                "sustainable_snacks",
                "nutrition_convenience",
            },
            "sports_nutrition": {
                "protein_nutrition",
                "fitness_wellness",
                "active_lifestyle",
                "energy_nutrition",
            },
            "beverages": {
                "functional_beverages",
                "hydration",
                "wellness_beverages",
            },
            "clean_foods": {
                "natural_foods",
                "plant_based_foods",
                "sustainable_products",
            },
            "convenience_foods": {
                "meal_solutions",
                "family_meals",
                "packaged_foods",
            },
        }

        related = related_categories.get(
            signal_category,
            set(),
        )

        if brand_category in related:
            return 0.7

        return 0.0

    @staticmethod
    def _keyword_score(
        signal_text: str,
        brand: dict[str, Any],
    ) -> float:
        """Calculate keyword overlap."""

        keywords = [
            str(keyword).lower()
            for keyword in brand.get(
                "keywords",
                [],
            )
        ]

        if not keywords:
            return 0.0

        matched = sum(
            1
            for keyword in keywords
            if keyword in signal_text
        )

        return min(
            matched / max(len(keywords), 1),
            1.0,
        )

    @staticmethod
    def _strategic_score(
        signal_text: str,
        brand: dict[str, Any],
    ) -> float:
        """Calculate strategic priority alignment."""

        priorities = [
            str(priority).lower()
            for priority in brand.get(
                "strategic_priorities",
                [],
            )
        ]

        if not priorities:
            return 0.0

        matched = sum(
            1
            for priority in priorities
            if priority in signal_text
        )

        return min(
            matched / max(len(priorities), 1),
            1.0,
        )

    @staticmethod
    def _consumer_score(
        signal_text: str,
        brand: dict[str, Any],
    ) -> float:
        """Estimate target-consumer alignment."""

        consumers = [
            str(consumer).lower().replace(
                "_",
                " ",
            )
            for consumer in brand.get(
                "target_consumer",
                [],
            )
        ]

        if not consumers:
            return 0.0

        matched = sum(
            1
            for consumer in consumers
            if consumer in signal_text
        )

        return min(
            matched / max(len(consumers), 1),
            1.0,
        )

    @staticmethod
    def _geography_score(
        signal: dict[str, Any],
        brand: dict[str, Any],
    ) -> float:
        """Estimate geographic alignment."""

        metadata = signal.get(
            "metadata",
            {},
        )

        signal_region = str(
            metadata.get(
                "region",
                "",
            )
        ).lower()

        if not signal_region:
            return 0.5

        brand_geographies = [
            str(location).lower().replace(
                "_",
                " ",
            )
            for location in brand.get(
                "geography",
                [],
            )
        ]

        if not brand_geographies:
            return 0.0

        if signal_region in brand_geographies:
            return 1.0

        if "india" in signal_region and "india" in brand_geographies:
            return 1.0

        return 0.0