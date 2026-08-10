from app.services.retrieval import FAISSRetriever

class FakeEmbeddingService:
    """
    Deterministic embedding service for unit tests.

    This keeps the test independent of downloaded ML models.
    """

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

def test_retriever_builds_index() -> None:
    retriever = FAISSRetriever(
        embedding_service=FakeEmbeddingService()
    )

    signals = [
        {
            "id": "signal_001",
            "title": "High protein snacks",
            "text": "Consumers want more protein snacks.",
            "category": "healthy_snacks",
            "signal_type": "consumer_trend",
            "source_type": "trend",
            "metadata": {},
        },
        {
            "id": "signal_002",
            "title": "Hydration beverages",
            "text": "Consumers want functional beverages.",
            "category": "beverages",
            "signal_type": "consumer_trend",
            "source_type": "trend",
            "metadata": {},
        },
    ]

    retriever.build_index(signals)

    assert retriever.index is not None
    assert len(retriever.documents) == 2

def test_retriever_returns_relevant_evidence() -> None:
    retriever = FAISSRetriever(
        embedding_service=FakeEmbeddingService()
    )

    signals = [
        {
            "id": "signal_001",
            "title": "High protein snacks",
            "text": "Consumers want more protein snacks.",
            "category": "healthy_snacks",
            "signal_type": "consumer_trend",
            "source_type": "trend",
            "metadata": {},
        },
        {
            "id": "signal_002",
            "title": "Hydration beverages",
            "text": "Consumers want functional beverages.",
            "category": "beverages",
            "signal_type": "consumer_trend",
            "source_type": "trend",
            "metadata": {},
        },
    ]

    retriever.build_index(signals)

    results = retriever.search(
        "high protein consumer demand",
        top_k=1,
    )

    assert len(results) == 1
    assert results[0].signal_id == "signal_001"
    assert results[0].score > 0.9

def test_empty_retriever_returns_no_results() -> None:
    retriever = FAISSRetriever(
        embedding_service=FakeEmbeddingService()
    )

    results = retriever.search(
        "protein",
        top_k=5,
    )

    assert results == []