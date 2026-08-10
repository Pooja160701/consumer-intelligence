import hashlib
from datetime import datetime, timezone
from typing import Any

class SignalNormalizer:
    """Normalize heterogeneous source records into a common signal format."""

    def normalize(
        self,
        record: dict[str, Any],
        source_type: str,
    ) -> dict[str, Any]:
        """Convert a raw source record into the canonical signal format."""

        title = str(
            record.get("title")
            or record.get("headline")
            or "Untitled signal"
        ).strip()

        text = str(
            record.get("text")
            or record.get("content")
            or record.get("description")
            or ""
        ).strip()

        category = str(
            record.get("category")
            or "general"
        ).strip().lower()

        signal_type = str(
            record.get("signal_type")
            or source_type
        ).strip().lower()

        url = record.get("url")

        published_at = record.get("published_at")

        if isinstance(published_at, datetime):
            published_at_value = published_at.isoformat()
        elif published_at:
            published_at_value = str(published_at)
        else:
            published_at_value = None

        metadata = record.get("metadata") or {}

        canonical_text = (
            f"{source_type}|"
            f"{title.lower()}|"
            f"{text.lower()}|"
            f"{category}"
        )

        signal_hash = hashlib.sha256(
            canonical_text.encode("utf-8")
        ).hexdigest()

        return {
            "id": f"signal_{signal_hash[:16]}",
            "source_type": source_type,
            "signal_type": signal_type,
            "title": title,
            "text": text,
            "category": category,
            "url": url,
            "published_at": published_at_value,
            "metadata": metadata,
            "content_hash": signal_hash,
            "ingested_at": datetime.now(timezone.utc).isoformat(),
        }