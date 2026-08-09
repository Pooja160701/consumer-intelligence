from datetime import datetime
from typing import Any
from sqlalchemy import JSON, DateTime, Float, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column
from app.services.database import Base

class Signal(Base):
    """Normalized consumer or market signal."""

    __tablename__ = "signals"

    id: Mapped[str] = mapped_column(
        String(100),
        primary_key=True,
    )

    source_id: Mapped[str] = mapped_column(
        ForeignKey("sources.id"),
        nullable=False,
        index=True,
    )

    signal_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )

    category: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True,
    )

    title: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    text: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    metadata_json: Mapped[dict[str, Any]] = mapped_column(
        JSON,
        nullable=False,
        default=dict,
    )

    confidence: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=0.0,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )