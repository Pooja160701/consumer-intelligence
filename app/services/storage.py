from datetime import datetime
from typing import Any
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.signal import Signal
from app.models.source import Source

class SignalStorage:
    """Persistence service for sources and normalized signals."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def source_exists(self, content_hash: str) -> bool:
        """Check whether a source with the given content hash exists."""

        statement = select(Source).where(
            Source.content_hash == content_hash
        )

        return self.db.scalar(statement) is not None

    def signal_exists(self, signal_id: str) -> bool:
        """Check whether a signal already exists."""

        statement = select(Signal).where(
            Signal.id == signal_id
        )

        return self.db.scalar(statement) is not None

    def save_source(
        self,
        signal: dict[str, Any],
    ) -> Source:
        """Persist a source record."""

        source = Source(
            id=f"source_{signal['content_hash'][:16]}",
            source_type=signal["source_type"],
            url=signal.get("url"),
            title=signal["title"],
            published_at=self._parse_datetime(
                signal.get("published_at")
            ),
            content_hash=signal["content_hash"],
        )

        self.db.add(source)

        return source

    def save_signal(
        self,
        signal: dict[str, Any],
        source_id: str,
    ) -> Signal:
        """Persist a normalized signal."""

        signal_model = Signal(
            id=signal["id"],
            source_id=source_id,
            signal_type=signal["signal_type"],
            category=signal["category"],
            title=signal["title"],
            text=signal["text"],
            metadata_json=signal.get("metadata", {}),
            confidence=float(
                signal.get("metadata", {}).get(
                    "confidence",
                    0.0,
                )
            ),
        )

        self.db.add(signal_model)

        return signal_model

    def save_signal_with_source(
        self,
        signal: dict[str, Any],
    ) -> tuple[Source | None, Signal | None]:
        """
        Persist a source and its signal.

        Existing records are skipped so repeated ingestion
        remains idempotent.
        """

        if self.source_exists(signal["content_hash"]):
            return None, None

        if self.signal_exists(signal["id"]):
            return None, None

        source = self.save_source(signal)

        self.db.flush()

        saved_signal = self.save_signal(
            signal,
            source_id=source.id,
        )

        self.db.commit()

        return source, saved_signal

    @staticmethod
    def _parse_datetime(
        value: str | None,
    ) -> datetime | None:
        """Parse an ISO datetime string."""

        if not value:
            return None

        normalized = value.replace("Z", "+00:00")

        return datetime.fromisoformat(normalized)