from functools import lru_cache
from pathlib import Path
from app.agents.workflow import IntelligenceWorkflow
from app.services.brand_registry import BrandRegistry
from app.services.database import SessionLocal
from app.services.embeddings import get_embedding_service
from app.services.llm import MockLLMProvider
from app.services.retrieval import FAISSRetriever

BRANDS_FILE = Path("data/brands.yaml")

@lru_cache(maxsize=1)
def get_brand_registry() -> BrandRegistry:
    """Return the cached configuration-driven brand registry."""

    return BrandRegistry(BRANDS_FILE)

@lru_cache(maxsize=1)
def get_workflow() -> IntelligenceWorkflow:
    """
    Build and cache the application intelligence workflow.

    PostgreSQL is the source of truth for signals.
    FAISS is rebuilt from persisted signals when the
    application workflow is initialized.
    """

    embedding_service = get_embedding_service()

    retriever = FAISSRetriever(
        embedding_service=embedding_service,
    )

    db = SessionLocal()

    try:
        retriever.build_index_from_database(db)
    finally:
        db.close()

    return IntelligenceWorkflow(
        retriever=retriever,
        llm=MockLLMProvider(),
    )