from datetime import datetime
from sqlalchemy import DateTime, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column
from app.services.database import Base

class Source(Base):
    """Represents an external information source."""

    __tablename__ = "sources"

    id: Mapped[str] = mapped_column(
        String(100),
        primary_key=True,
    )

    source_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )

    url: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    title: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    published_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    content_hash: Mapped[str] = mapped_column(
        String(128),
        nullable=False,
        index=True,
    )

    ingested_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )