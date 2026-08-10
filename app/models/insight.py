from datetime import datetime
from typing import Any
from sqlalchemy import (
    DateTime,
    Float,
    ForeignKey,
    JSON,
    String,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column
from app.services.database import Base

class Insight(Base):
    """Business-ready intelligence generated from one or more signals."""

    __tablename__ = "insights"

    id: Mapped[str] = mapped_column(
        String(100),
        primary_key=True,
    )

    brand_id: Mapped[str] = mapped_column(
        ForeignKey("brands.id"),
        nullable=False,
        index=True,
    )

    signal_id: Mapped[str] = mapped_column(
        ForeignKey("signals.id"),
        nullable=False,
        index=True,
    )

    summary: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    observation: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    interpretation: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    opportunity: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    risk: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    recommendation: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    impact_score: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=0.0,
    )

    relevance_score: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=0.0,
    )

    confidence_score: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=0.0,
    )

    priority: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="P3",
        index=True,
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="PENDING_REVIEW",
        index=True,
    )

    evidence: Mapped[list[dict[str, Any]]] = mapped_column(
        JSON,
        nullable=False,
        default=list,
    )

    prompt_version: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        default="insight_generation:v1",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )