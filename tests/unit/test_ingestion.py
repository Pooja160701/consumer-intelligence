from pathlib import Path
from app.ingestion.loader import SignalLoader
from app.intelligence.deduplication import SignalDeduplicator

SIGNAL_FILE = Path("data/raw/sample_signals.json")

def test_signal_loading() -> None:
    loader = SignalLoader()

    signals = loader.load_json(
        SIGNAL_FILE,
        source_type="mixed",
    )

    assert len(signals) == 7
    assert signals[0]["title"] == "High-protein snacks gain consumer interest"
    assert signals[0]["category"] == "healthy_snacks"

def test_signal_deduplication() -> None:
    loader = SignalLoader()

    signals = loader.load_json(
        SIGNAL_FILE,
        source_type="mixed",
    )

    deduplicator = SignalDeduplicator()

    unique_signals = deduplicator.deduplicate(signals)

    assert len(unique_signals) == 6

def test_signal_contains_content_hash() -> None:
    loader = SignalLoader()

    signals = loader.load_json(
        SIGNAL_FILE,
        source_type="mixed",
    )

    assert signals
    assert signals[0]["content_hash"]
    assert len(signals[0]["content_hash"]) == 64