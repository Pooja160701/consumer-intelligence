from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column
from app.services.database import Base

class HumanReview(Base):
    """Human decision associated with an AI-generated insight."""

    __tablename__ = "human_reviews"

    id: Mapped[str] = mapped_column(
        String(100),
        primary_key=True,
    )

    insight_id: Mapped[str] = mapped_column(
        ForeignKey("insights.id"),
        nullable=False,
        index=True,
    )

    reviewer_action: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    comment: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )