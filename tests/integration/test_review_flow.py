from uuid import uuid4
from fastapi.testclient import TestClient
from app.main import app
from app.services.database import SessionLocal
from app.models.brand import Brand
from app.models.insight import Insight
from app.models.signal import Signal
from app.models.source import Source
from app.models.review import HumanReview

def create_test_data() -> tuple[str, str, str]:
    """
    Create complete test data in foreign-key dependency order.

    Dependency graph:

        Source
          ↓
        Signal

        Brand
          ↓
        Insight
          ↑
        Signal
    """

    db = SessionLocal()

    source_id = f"test_source_{uuid4().hex[:8]}"
    brand_id = f"test_brand_{uuid4().hex[:8]}"
    signal_id = f"test_signal_{uuid4().hex[:8]}"
    insight_id = f"test_insight_{uuid4().hex[:8]}"

    try:
        source = Source(
            id=source_id,
            source_type="synthetic_test",
            url="https://example.com/test-signal",
            title="Synthetic Consumer Trend Test Source",
            content_hash=uuid4().hex,
        )

        db.add(source)
        db.flush()

        brand = Brand(
            id=brand_id,
            name="Review Test Brand",
            category="healthy_snacks",
            description=(
                "Synthetic brand used for human-review "
                "integration testing."
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

        insight = Insight(
            id=insight_id,
            brand_id=brand_id,
            signal_id=signal_id,
            summary=(
                "Protein snack demand is increasing."
            ),
            observation=(
                "Demand for protein snacks is increasing."
            ),
            interpretation=(
                "The signal aligns with the brand's "
                "health positioning."
            ),
            opportunity=(
                "Explore convenient high-protein "
                "product offerings."
            ),
            risk=(
                "Moving without additional validation "
                "could lead to unnecessary investment."
            ),
            recommendation=(
                "Validate the trend with additional "
                "evidence before making a major investment."
            ),
            impact_score=0.85,
            relevance_score=0.92,
            confidence_score=0.88,
            priority="P1",
            status="PENDING_REVIEW",
            evidence=[],
        )

        db.add(insight)
        db.flush()
        db.commit()

        return (
            brand_id,
            signal_id,
            insight_id,
        )

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()

def cleanup_test_data(
    brand_id: str,
    signal_id: str,
    insight_id: str,
) -> None:
    """Remove integration-test data in foreign-key dependency order."""

    db = SessionLocal()

    try:
        signal = db.get(
            Signal,
            signal_id,
        )

        source_id = (
            signal.source_id
            if signal is not None
            else None
        )

        reviews = (
            db.query(HumanReview)
            .filter(
                HumanReview.insight_id == insight_id
            )
            .all()
        )

        for review in reviews:
            db.delete(review)

        db.flush()

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

        if source_id is not None:
            source = db.get(
                Source,
                source_id,
            )

            if source is not None:
                db.delete(source)

        brand = db.get(
            Brand,
            brand_id,
        )

        if brand is not None:
            db.delete(brand)

        db.commit()

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()

def test_review_can_be_approved() -> None:
    """
    A persisted insight can receive an APPROVE decision.
    """

    brand_id, signal_id, insight_id = create_test_data()

    try:
        client = TestClient(app)

        response = client.post(
            "/api/v1/reviews",
            json={
                "insight_id": insight_id,
                "reviewer_action": "APPROVE",
                "comment": "Evidence is sufficient.",
            },
        )

        assert response.status_code == 200

        body = response.json()

        assert body["insight_id"] == insight_id
        assert body["reviewer_action"] == "APPROVE"
        assert body["status"] == "RECORDED"

    finally:
        cleanup_test_data(
            brand_id,
            signal_id,
            insight_id,
        )

def test_review_can_be_rejected() -> None:
    """
    A persisted insight can receive a REJECT decision.
    """

    brand_id, signal_id, insight_id = create_test_data()

    try:
        client = TestClient(app)

        response = client.post(
            "/api/v1/reviews",
            json={
                "insight_id": insight_id,
                "reviewer_action": "REJECT",
                "comment": "Insufficient supporting evidence.",
            },
        )

        assert response.status_code == 200

        body = response.json()

        assert body["reviewer_action"] == "REJECT"
        assert body["status"] == "RECORDED"

    finally:
        cleanup_test_data(
            brand_id,
            signal_id,
            insight_id,
        )

def test_review_can_modify_insight() -> None:
    """
    A reviewer can mark an insight for modification.
    """

    brand_id, signal_id, insight_id = create_test_data()

    try:
        client = TestClient(app)

        response = client.post(
            "/api/v1/reviews",
            json={
                "insight_id": insight_id,
                "reviewer_action": "MODIFY",
                "comment": "Recommendation needs refinement.",
            },
        )

        assert response.status_code == 200

        body = response.json()

        assert body["reviewer_action"] == "MODIFY"

    finally:
        cleanup_test_data(
            brand_id,
            signal_id,
            insight_id,
        )

def test_review_returns_404_for_unknown_insight() -> None:
    """
    Reviews cannot be created for an unknown insight.
    """

    client = TestClient(app)

    response = client.post(
        "/api/v1/reviews",
        json={
            "insight_id": "does_not_exist",
            "reviewer_action": "APPROVE",
        },
    )

    assert response.status_code == 404

def test_review_is_persisted() -> None:
    """
    A successful review must actually be stored in PostgreSQL.
    """

    brand_id, signal_id, insight_id = create_test_data()

    try:
        client = TestClient(app)

        response = client.post(
            "/api/v1/reviews",
            json={
                "insight_id": insight_id,
                "reviewer_action": "APPROVE",
                "comment": "Approved after review.",
            },
        )

        assert response.status_code == 200

        review_id = response.json()["id"]

        from app.models.review import HumanReview

        db = SessionLocal()

        review = db.get(
            HumanReview,
            review_id,
        )

        assert review is not None
        assert review.insight_id == insight_id
        assert review.reviewer_action == "APPROVE"
        assert review.comment == "Approved after review."

        db.close()

    finally:
        cleanup_test_data(
            brand_id,
            signal_id,
            insight_id,
        )