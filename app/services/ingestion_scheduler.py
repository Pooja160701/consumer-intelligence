from __future__ import annotations
import logging
from pathlib import Path
from apscheduler.schedulers.background import BackgroundScheduler
from app.ingestion.pipeline import IngestionPipeline
from app.services.database import SessionLocal

logger = logging.getLogger(__name__)

scheduler = BackgroundScheduler()

def run_scheduled_ingestion() -> None:
    """Execute the configured recurring ingestion job."""

    db = SessionLocal()

    try:
        pipeline = IngestionPipeline(db)

        source_file = Path(
            "data/raw/consumer_signals.json"
        )

        if not source_file.exists():
            logger.warning(
                "Scheduled ingestion skipped: %s does not exist",
                source_file,
            )
            return

        result = pipeline.ingest_json(
            source_file,
            source_type="scheduled",
        )

        db.commit()

        logger.info(
            "Scheduled ingestion completed: %s",
            result,
        )

    except Exception:
        db.rollback()
        logger.exception(
            "Scheduled ingestion failed"
        )

    finally:
        db.close()

def start_ingestion_scheduler() -> None:
    """Start recurring consumer-signal ingestion."""

    if scheduler.running:
        return

    scheduler.add_job(
        run_scheduled_ingestion,
        trigger="interval",
        hours=6,
        id="consumer-signal-ingestion",
        replace_existing=True,
        max_instances=1,
        coalesce=True,
    )

    scheduler.start()

    logger.info(
        "Consumer intelligence scheduler started "
        "(every 6 hours)"
    )

def stop_ingestion_scheduler() -> None:
    """Stop recurring ingestion."""

    if scheduler.running:
        scheduler.shutdown(wait=False)

        logger.info(
            "Consumer intelligence scheduler stopped"
        )