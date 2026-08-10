from typing import Any
from app.ingestion.base import BaseSourceAdapter

class TrendSourceAdapter(BaseSourceAdapter):
    """Synthetic trend source used by the POC."""

    def __init__(self, records: list[dict[str, Any]] | None = None) -> None:
        self.records = records or []

    def fetch(self) -> list[dict[str, Any]]:
        """Return available trend records."""
        return self.records