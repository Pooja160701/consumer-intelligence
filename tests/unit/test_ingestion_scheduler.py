from unittest.mock import MagicMock, patch
from app.services import ingestion_scheduler

def test_scheduler_starts_and_registers_job():
    fake_scheduler = MagicMock()
    fake_scheduler.running = False

    with patch.object(
        ingestion_scheduler,
        "scheduler",
        fake_scheduler,
    ):
        ingestion_scheduler.start_ingestion_scheduler()

    fake_scheduler.add_job.assert_called_once()

    kwargs = fake_scheduler.add_job.call_args.kwargs

    assert kwargs["trigger"] == "interval"
    assert kwargs["hours"] == 6
    assert kwargs["id"] == "consumer-signal-ingestion"
    assert kwargs["max_instances"] == 1
    assert kwargs["coalesce"] is True

    fake_scheduler.start.assert_called_once()

def test_scheduler_does_not_start_twice():
    fake_scheduler = MagicMock()
    fake_scheduler.running = True

    with patch.object(
        ingestion_scheduler,
        "scheduler",
        fake_scheduler,
    ):
        ingestion_scheduler.start_ingestion_scheduler()

    fake_scheduler.add_job.assert_not_called()
    fake_scheduler.start.assert_not_called()

def test_scheduler_stops():
    fake_scheduler = MagicMock()
    fake_scheduler.running = True

    with patch.object(
        ingestion_scheduler,
        "scheduler",
        fake_scheduler,
    ):
        ingestion_scheduler.stop_ingestion_scheduler()

    fake_scheduler.shutdown.assert_called_once_with(
        wait=False
    )