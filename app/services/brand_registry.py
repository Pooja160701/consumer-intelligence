from pathlib import Path
from typing import Any
import yaml

class BrandRegistry:
    """Loads and manages configuration-driven brand profiles."""

    def __init__(self, config_path: str | Path) -> None:
        self.config_path = Path(config_path)
        self._brands: dict[str, dict[str, Any]] = {}

        self._load()

    def _load(self) -> None:
        """Load brand configuration from YAML."""

        if not self.config_path.exists():
            raise FileNotFoundError(
                f"Brand configuration not found: {self.config_path}"
            )

        with self.config_path.open("r", encoding="utf-8") as file:
            configuration = yaml.safe_load(file) or {}

        brands = configuration.get("brands", [])

        for brand in brands:
            brand_id = brand.get("id")

            if not brand_id:
                raise ValueError("Every brand must have an 'id'.")

            if brand_id in self._brands:
                raise ValueError(
                    f"Duplicate brand ID detected: {brand_id}"
                )

            self._brands[brand_id] = brand

    def get_brand(self, brand_id: str) -> dict[str, Any]:
        """Return a brand configuration by ID."""

        if brand_id not in self._brands:
            raise KeyError(f"Unknown brand: {brand_id}")

        return self._brands[brand_id]

    def list_brands(self) -> list[dict[str, Any]]:
        """Return all configured brands."""

        return list(self._brands.values())

    def brand_count(self) -> int:
        """Return the number of configured brands."""

        return len(self._brands)

    def find_relevant_brands(
        self,
        text: str,
        category: str | None = None,
    ) -> list[dict[str, Any]]:
        """
        Find brands whose configuration is relevant to a signal.

        Relevance is determined using category and configured keywords.
        """

        normalized_text = text.lower()

        relevant: list[dict[str, Any]] = []

        for brand in self._brands.values():
            score = 0

            brand_category = brand.get("category", "").lower()

            if category and category.lower() == brand_category:
                score += 2

            for keyword in brand.get("keywords", []):
                if keyword.lower() in normalized_text:
                    score += 1

            if score > 0:
                relevant.append(
                    {
                        "brand": brand,
                        "relevance_score": score,
                    }
                )

        return sorted(
            relevant,
            key=lambda item: item["relevance_score"],
            reverse=True,
        )