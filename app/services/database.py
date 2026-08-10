from collections.abc import Generator
from sqlalchemy import create_engine, text
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
    Provide a database session.

    The session is always closed after use.
    """
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

def check_database_connection() -> bool:
    """Check whether PostgreSQL is reachable."""
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return True
    except Exception:
        return False

def create_tables() -> None:
    """Create all SQLAlchemy tables for local development."""
    # Import models before creating tables so SQLAlchemy
    # knows about all mapped classes.
    from app import models  # noqa: F401

    Base.metadata.create_all(bind=engine)