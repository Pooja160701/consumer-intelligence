from app.agents.workflow import IntelligenceWorkflow
from app.services.retrieval import FAISSRetriever

class FakeEmbeddingService:
    """Deterministic embeddings for workflow tests."""

    def embed_texts(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        embeddings = []

        for text in texts:
            normalized = text.lower()

            if "protein" in normalized:
                embeddings.append(
                    [1.0, 0.0, 0.0]
                )
            elif "hydration" in normalized:
                embeddings.append(
                    [0.0, 1.0, 0.0]
                )
            else:
                embeddings.append(
                    [0.1, 0.1, 0.1]
                )

        return embeddings

    def embed_text(
        self,
        text: str,
    ) -> list[float]:
        return self.embed_texts([text])[0]

def create_retriever() -> FAISSRetriever:
    retriever = FAISSRetriever(
        embedding_service=FakeEmbeddingService()
    )

    retriever.build_index(
        [
            {
                "id": "signal_evidence_001",
                "title": "Protein demand is increasing",
                "text": (
                    "Consumers increasingly seek "
                    "high protein snacks."
                ),
                "category": "healthy_snacks",
                "signal_type": "consumer_trend",
                "source_type": "trend",
                "metadata": {
                    "region": "India"
                },
            }
        ]
    )

    return retriever

def test_intelligence_workflow_generates_insight() -> None:
    workflow = IntelligenceWorkflow(
        retriever=create_retriever()
    )

    signal = {
        "id": "signal_001",
        "title": "High protein snacks gain popularity",
        "text": (
            "Consumers increasingly want "
            "convenient high protein snacks."
        ),
        "category": "healthy_snacks",
        "signal_type": "consumer_trend",
        "metadata": {
            "region": "India"
        },
    }

    brand = {
        "id": "brand_001",
        "name": "VitaBite",
        "category": "healthy_snacks",
        "strategic_priorities": [
            "health",
            "protein",
            "convenience",
        ],
        "keywords": [
            "protein",
            "healthy snacks",
            "high protein",
        ],
        "target_consumer": [
            "young_adults",
            "working_professionals",
        ],
        "geography": [
            "india",
        ],
    }

    result = workflow.run(
        signal=signal,
        brand=brand,
    )

    assert result["observation"]
    assert result["interpretation"]
    assert result["opportunity"]
    assert result["risk"]
    assert result["recommendation"]

    assert result["evidence"]
    assert result["relevance"]

    assert result["priority"] in {
        "P1",
        "P2",
        "P3",
        "P4",
    }

    assert 0.0 <= result["confidence_score"] <= 1.0
    assert 0.0 <= result["priority_score"] <= 1.0

def test_workflow_contains_expected_nodes() -> None:
    workflow = IntelligenceWorkflow(
        retriever=create_retriever()
    )

    graph_nodes = workflow.graph.nodes

    assert "signal_analysis" in graph_nodes
    assert "brand_context" in graph_nodes
    assert "evidence_retrieval" in graph_nodes
    assert "insight_generation" in graph_nodes
    assert "prioritization" in graph_nodes

def test_workflow_uses_structured_llm_insight() -> None:
    workflow = IntelligenceWorkflow(
        retriever=create_retriever()
    )

    signal = {
        "id": "signal_002",
        "title": "Protein demand is increasing",
        "text": (
            "Consumers increasingly seek "
            "high protein products."
        ),
        "category": "healthy_snacks",
        "signal_type": "consumer_trend",
        "metadata": {
            "region": "India"
        },
    }

    brand = {
        "id": "brand_001",
        "name": "VitaBite",
        "category": "healthy_snacks",
        "strategic_priorities": [
            "health",
            "protein",
        ],
        "keywords": [
            "protein",
            "healthy snacks",
        ],
        "target_consumer": [
            "young_adults",
        ],
        "geography": [
            "india",
        ],
    }

    result = workflow.run(
        signal=signal,
        brand=brand,
    )

    assert result["observation"]
    assert result["interpretation"]
    assert result["opportunity"]
    assert result["risk"]
    assert result["recommendation"]

    assert (
        result["prompt_version"]
        == "insight_generation:v1"
    )

    assert result["evidence_count"] >= 0

    assert isinstance(
        result["grounded"],
        bool,
    )