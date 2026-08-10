from uuid import uuid4
from fastapi.testclient import TestClient
from app.api.dependencies import get_workflow
from app.main import app
from app.models.insight import Insight
from app.models.signal import Signal
from app.models.source import Source
from app.services.database import SessionLocal
from app.models.brand import Brand

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

def test_insight_persists_prompt_version() -> None:
    """
    A generated insight must persist its prompt version
    in PostgreSQL.
    """

    app.dependency_overrides[
        get_workflow
    ] = lambda: FakeWorkflow()

    db = SessionLocal()

    source_id = f"test_source_{uuid4().hex[:8]}"
    signal_id = f"test_signal_{uuid4().hex[:8]}"
    insight_id = None

    try:
        brand = Brand(
            id="brand_001",
            name="Prompt Version Test Brand",
            category="healthy_snacks",
            description=(
                "Synthetic brand used for prompt version testing."
            ),
            configuration={
                "keywords": [
                    "protein",
                    "healthy snacks",
                    "high protein",
                ],
                "strategic_priorities": [
                    "health",
                    "protein",
                    "convenience",
                ],
                "target_consumer": [
                    "young_adults",
                    "working_professionals",
                ],
                "geography": [
                    "india",
                ],
            },
        )

        db.add(brand)
        db.flush()

        source = Source(
            id=source_id,
            source_type="synthetic_test",
            url="https://example.com/prompt-version-test",
            title="Prompt Version Test Source",
            content_hash=uuid4().hex,
        )

        db.add(source)
        db.flush()

        signal = Signal(
            id=signal_id,
            source_id=source_id,
            signal_type="consumer_trend",
            category="healthy_snacks",
            title="Protein snack demand is increasing",
            text=(
                "Consumers increasingly want "
                "convenient high protein snacks."
            ),
            metadata_json={
                "region": "India",
                "test": True,
            },
            confidence=0.95,
        )

        db.add(signal)
        db.flush()

        db.commit()

        client = TestClient(app)

        response = client.post(
            "/api/v1/insights",
            json={
                "brand_id": "brand_001",
                "signal": {
                    "title": (
                        "Protein snack demand is increasing"
                    ),
                    "text": (
                        "Consumers increasingly want "
                        "convenient high protein snacks."
                    ),
                    "category": "healthy_snacks",
                    "signal_type": "consumer_trend",
                    "metadata": {
                        "signal_id": signal_id,
                        "region": "India",
                    },
                },
            },
        )

        print("STATUS:", response.status_code)
        print("BODY:", response.text)

        assert response.status_code == 200

        body = response.json()

        assert body["prompt_version"] == (
            "insight_generation:v1"
        )

        insight_id = body["insight_id"]

        db.expire_all()

        insight = db.get(
            Insight,
            insight_id,
        )

        assert insight is not None

        assert insight.prompt_version == (
            "insight_generation:v1"
        )

        assert insight.signal_id == signal_id
        assert insight.brand_id == "brand_001"

    finally:
        db.rollback()

        if insight_id is not None:
            insight = db.get(
                Insight,
                insight_id,
            )

            if insight is not None:
                db.delete(insight)
                db.flush()

        signal = db.get(
            Signal,
            signal_id,
        )

        if signal is not None:
            db.delete(signal)
            db.flush()

        source = db.get(
            Source,
            source_id,
        )

        if source is not None:
            db.delete(source)
            db.flush()

        brand = db.get(
            Brand,
            "brand_001",
        )

        if brand is not None:
            db.delete(brand)

        db.commit()
        db.close()

        app.dependency_overrides.clear()