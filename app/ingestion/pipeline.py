from pathlib import Path
from typing import Any
from sqlalchemy.orm import Session
from app.ingestion.loader import SignalLoader
from app.intelligence.deduplication import SignalDeduplicator
from app.services.storage import SignalStorage

class IngestionPipeline:
    """End-to-end signal ingestion pipeline."""

    def __init__(
        self,
        db: Session,
        loader: SignalLoader | None = None,
        deduplicator: SignalDeduplicator | None = None,
    ) -> None:
        self.db = db
        self.loader = loader or SignalLoader()
        self.deduplicator = (
            deduplicator or SignalDeduplicator()
        )
        self.storage = SignalStorage(db)

    def ingest_json(
        self,
        file_path: str | Path,
        source_type: str = "mixed",
    ) -> dict[str, Any]:
        """
        Load, normalize, deduplicate and persist signals.
        """

        signals = self.loader.load_json(
            file_path,
            source_type=source_type,
        )

        unique_signals = self.deduplicator.deduplicate(
            signals
        )

        stored_sources = 0
        stored_signals = 0
        skipped_signals = 0

        for signal in unique_signals:
            source, saved_signal = (
                self.storage.save_signal_with_source(
                    signal
                )
            )

            if source and saved_signal:
                stored_sources += 1
                stored_signals += 1
            else:
                skipped_signals += 1

        return {
            "input_records": len(signals),
            "unique_records": len(unique_signals),
            "stored_sources": stored_sources,
            "stored_signals": stored_signals,
            "skipped_records": skipped_signals,
        }