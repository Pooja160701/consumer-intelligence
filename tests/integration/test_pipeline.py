from pathlib import Path
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from app.ingestion.pipeline import IngestionPipeline
from app.models.signal import Signal
from app.models.source import Source
from app.services.database import Base

SIGNAL_FILE = Path("data/raw/sample_signals.json")

def test_ingestion_pipeline_persists_signals() -> None:
    engine = create_engine(
        "sqlite:///:memory:",
        future=True,
    )

    Base.metadata.create_all(engine)

    with Session(engine) as session:
        pipeline = IngestionPipeline(session)

        result = pipeline.ingest_json(
            SIGNAL_FILE,
            source_type="mixed",
        )

        assert result["input_records"] == 7
        assert result["unique_records"] == 6
        assert result["stored_sources"] == 6
        assert result["stored_signals"] == 6

        sources = session.scalars(
            select(Source)
        ).all()

        signals = session.scalars(
            select(Signal)
        ).all()

        assert len(sources) == 6
        assert len(signals) == 6

def test_ingestion_pipeline_is_idempotent() -> None:
    engine = create_engine(
        "sqlite:///:memory:",
        future=True,
    )

    Base.metadata.create_all(engine)

    with Session(engine) as session:
        pipeline = IngestionPipeline(session)

        first_result = pipeline.ingest_json(
            SIGNAL_FILE,
            source_type="mixed",
        )

        second_result = pipeline.ingest_json(
            SIGNAL_FILE,
            source_type="mixed",
        )

        assert first_result["stored_signals"] == 6
        assert second_result["stored_signals"] == 0
        assert second_result["skipped_records"] == 6