from collections.abc import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker
from app.config.settings import settings

class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""

    pass

engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
    future=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    class_=Session,
    autoflush=False,
    autocommit=False,
)

def get_db() -> Generator[Session, None, None]:
    """
    Provide a database session for API requests.

    The session is always closed after the request completes.
    """
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

def create_tables() -> None:
    """Create database tables for local development."""
    Base.metadata.create_all(bind=engine)