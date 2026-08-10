from typing import Any

class SignalDeduplicator:
    """Remove duplicate signals using their content hash."""

    def deduplicate(
        self,
        signals: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        """Return only unique signals."""

        seen_hashes: set[str] = set()
        unique_signals: list[dict[str, Any]] = []

        for signal in signals:
            content_hash = signal.get("content_hash")

            if not content_hash:
                unique_signals.append(signal)
                continue

            if content_hash in seen_hashes:
                continue

            seen_hashes.add(content_hash)
            unique_signals.append(signal)

        return unique_signals