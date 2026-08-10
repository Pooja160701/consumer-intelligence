from fastapi.testclient import TestClient
from app.api.dependencies import get_workflow
from app.main import app

class FakeWorkflow:
    """Deterministic workflow for API tests."""

    def run(
        self,
        signal: dict,
        brand: dict,
    ) -> dict:
        return {
            "observation": "Protein demand is increasing.",
            "interpretation": (
                "The signal is relevant to the brand."
            ),
            "opportunity": (
                "Evaluate a protein-focused offering."
            ),
            "risk": (
                "The trend may not persist."
            ),
            "recommendation": (
                "Validate with additional evidence."
            ),
            "relevance": {
                "overall_score": 0.91,
            },
            "confidence_score": 0.88,
            "priority_score": 0.90,
            "priority": "P1",
            "evidence_count": 1,
            "grounded": True,
            "prompt_version": (
                "insight_generation:v1"
            ),
            "evidence": [
                {
                    "signal_id": "evidence_001",
                    "title": (
                        "Protein demand is increasing"
                    ),
                    "text": (
                        "Consumers increasingly seek "
                        "high protein snacks."
                    ),
                    "category": "healthy_snacks",
                    "source_type": "trend",
                    "score": 0.94,
                    "metadata": {},
                }
            ],
        }

def test_health_endpoint() -> None:
    client = TestClient(app)

    response = client.get(
        "/api/v1/health"
    )

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok"
    }

def test_insight_endpoint() -> None:
    app.dependency_overrides[
        get_workflow
    ] = lambda: FakeWorkflow()

    client = TestClient(app)

    response = client.post(
        "/api/v1/insights",
        json={
            "brand_id": "brand_001",
            "signal": {
                "title": (
                    "High protein snacks "
                    "gain popularity"
                ),
                "text": (
                    "Consumers increasingly want "
                    "protein-rich snacks."
                ),
                "category": "healthy_snacks",
                "signal_type": "consumer_trend",
                "metadata": {
                    "region": "India"
                },
            },
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["brand_id"] == "brand_001"
    assert body["priority"] == "P1"
    assert body["grounded"] is True
    assert body["evidence_count"] == 1
    assert body["prompt_version"] == (
        "insight_generation:v1"
    )

    assert body["recommendation"]

    app.dependency_overrides.clear()