from functools import lru_cache
from app.agents.workflow import IntelligenceWorkflow
from app.services.database import SessionLocal
from app.services.embeddings import get_embedding_service
from app.services.llm import MockLLMProvider
from app.services.retrieval import FAISSRetriever

@lru_cache(maxsize=1)
def get_workflow() -> IntelligenceWorkflow:
    """
    Build and cache the application intelligence workflow.

    PostgreSQL is the source of truth. FAISS is rebuilt from
    persisted signals when the application initializes.
    """

    embedding_service = get_embedding_service()

    retriever = FAISSRetriever(
        embedding_service=embedding_service,
    )

    db = SessionLocal()

    try:
        retriever.build_index_from_database(
            db
        )
    finally:
        db.close()

    return IntelligenceWorkflow(
        retriever=retriever,
        llm=MockLLMProvider(),
    )