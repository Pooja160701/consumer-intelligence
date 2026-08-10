import json
from pathlib import Path
from typing import Any
from app.ingestion.base import BaseSourceAdapter
from app.ingestion.normalizer import SignalNormalizer

class SignalLoader:
    """Fetch and normalize signals from source adapters."""

    def __init__(
        self,
        normalizer: SignalNormalizer | None = None,
    ) -> None:
        self.normalizer = normalizer or SignalNormalizer()

    def load(
        self,
        adapter: BaseSourceAdapter,
        source_type: str,
    ) -> list[dict[str, Any]]:
        """Fetch raw records and normalize them."""

        raw_records = adapter.fetch()

        return [
            self.normalizer.normalize(
                record,
                source_type=source_type,
            )
            for record in raw_records
        ]

    def load_json(
        self,
        file_path: str | Path,
        source_type: str,
    ) -> list[dict[str, Any]]:
        """Load and normalize records from a JSON file."""

        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(
                f"Signal data file not found: {path}"
            )

        with path.open("r", encoding="utf-8") as file:
            records = json.load(file)

        if not isinstance(records, list):
            raise ValueError(
                "Signal JSON must contain a list of records."
            )

        return [
            self.normalizer.normalize(
                record,
                source_type=source_type,
            )
            for record in records
        ]