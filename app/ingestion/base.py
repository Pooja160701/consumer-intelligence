from abc import ABC, abstractmethod
from typing import Any

class BaseSourceAdapter(ABC):
    """Base interface for all intelligence data sources."""

    @abstractmethod
    def fetch(self) -> list[dict[str, Any]]:
        """
        Fetch raw records from the source.

        Implementations should return dictionaries containing
        source-specific raw data.
        """
        raise NotImplementedError