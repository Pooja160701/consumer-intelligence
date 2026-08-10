from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from app.ingestion.pipeline import IngestionPipeline
from app.services.database import Base
from app.services.retrieval import FAISSRetriever

SIGNAL_FILE = Path("data/raw/sample_signals.json")

class FakeEmbeddingService:
    """Deterministic embedding service for integration tests."""

    def embed_texts(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        embeddings = []

        for text in texts:
            normalized = text.lower()

            if "protein" in normalized:
                embeddings.append([1.0, 0.0, 0.0])

            elif (
                "beverage" in normalized
                or "hydration" in normalized
            ):
                embeddings.append([0.0, 1.0, 0.0])

            elif "sustainable" in normalized:
                embeddings.append([0.0, 0.0, 1.0])

            else:
                embeddings.append([0.1, 0.1, 0.1])

        return embeddings

    def embed_text(
        self,
        text: str,
    ) -> list[float]:
        return self.embed_texts([text])[0]

def create_test_database():
    """Create an isolated in-memory database."""

    engine = create_engine(
        "sqlite:///:memory:",
        future=True,
    )

    Base.metadata.create_all(engine)

    return engine

def test_faiss_index_can_be_built_from_database() -> None:
    engine = create_test_database()

    with Session(engine) as session:
        pipeline = IngestionPipeline(session)

        ingestion_result = pipeline.ingest_json(
            SIGNAL_FILE,
            source_type="mixed",
        )

        assert ingestion_result["stored_signals"] == 6

        retriever = FAISSRetriever(
            embedding_service=FakeEmbeddingService()
        )

        indexed_count = (
            retriever.build_index_from_database(
                session
            )
        )

        assert indexed_count == 6
        assert retriever.index is not None
        assert len(retriever.documents) == 6

def test_database_backed_retrieval_returns_evidence() -> None:
    engine = create_test_database()

    with Session(engine) as session:
        pipeline = IngestionPipeline(session)

        pipeline.ingest_json(
            SIGNAL_FILE,
            source_type="mixed",
        )

        retriever = FAISSRetriever(
            embedding_service=FakeEmbeddingService()
        )

        retriever.build_index_from_database(
            session
        )

        results = retriever.search(
            "high protein snacks",
            top_k=2,
        )

        assert results
        assert results[0].signal_id
        assert results[0].title
        assert results[0].text
        assert results[0].score > 0.0