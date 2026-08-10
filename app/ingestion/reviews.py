from typing import Any
from app.ingestion.base import BaseSourceAdapter

class ReviewSourceAdapter(BaseSourceAdapter):
    """Synthetic consumer-review source used by the POC."""

    def __init__(self, records: list[dict[str, Any]] | None = None) -> None:
        self.records = records or []

    def fetch(self) -> list[dict[str, Any]]:
        """Return available consumer review records."""
        return self.records