from uuid import uuid4
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.dependencies import (
    get_brand_registry,
    get_workflow,
)
from app.api.routes.reviews import router as reviews_router
from app.api.schemas import InsightRequest, InsightResponse
from app.models.insight import Insight
from app.models.signal import Signal
from app.models.source import Source
from app.services.database import get_db

router = APIRouter(
    prefix="/api/v1",
    tags=["intelligence"],
)

router.include_router(reviews_router)

@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}

@router.post(
    "/insights",
    response_model=InsightResponse,
)
def generate_insight(
    request: InsightRequest,
    workflow=Depends(get_workflow),
    brand_registry=Depends(get_brand_registry),
    db: Session = Depends(get_db),
) -> InsightResponse:

    try:
        brand = brand_registry.get_brand(request.brand_id)
    except KeyError as exc:
        raise HTTPException(
            status_code=404,
            detail=f"Unknown brand: {request.brand_id}",
        ) from exc

    signal_data = request.signal.model_dump()
    metadata = dict(signal_data.get("metadata") or {})

    signal_id = metadata.get("signal_id")

    if signal_id:
        existing_signal = db.get(Signal, signal_id)

        if existing_signal is None:
            raise HTTPException(
                status_code=404,
                detail=f"Signal not found: {signal_id}",
            )

    else:
        source_id = f"source_{uuid4().hex}"

        source = Source(
            id=source_id,
            source_type=metadata.get(
                "source_type",
                "synthetic_market_signal",
            ),
            url=metadata.get("url"),
            title=signal_data["title"],
            content_hash=uuid4().hex,
        )

        db.add(source)

        signal_id = f"signal_{uuid4().hex}"

        signal = Signal(
            id=signal_id,
            source_id=source_id,
            signal_type=signal_data["signal_type"],
            category=signal_data["category"],
            title=signal_data["title"],
            text=signal_data["text"],
            metadata_json=metadata,
            confidence=float(
                metadata.get("confidence", 0.0)
            ),
        )

        db.add(signal)
        db.flush()

    try:
        result = workflow.run(
            signal={
                **signal_data,
                "metadata": {
                    **metadata,
                    "signal_id": signal_id,
                },
            },
            brand=brand,
        )

    except Exception as exc:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail="Failed to generate intelligence insight.",
        ) from exc

    relevance = result.get("relevance", {})
    evidence = result.get("evidence", [])

    relevance_score = float(
        relevance.get("overall_score", 0.0)
    )

    confidence_score = float(
        result.get("confidence_score", 0.0)
    )

    priority_score = float(
        result.get("priority_score", 0.0)
    )

    priority = result.get("priority", "P4")

    insight_id = f"insight_{uuid4().hex}"

    try:
        insight = Insight(
            id=insight_id,
            brand_id=brand["id"],
            signal_id=signal_id,
            summary=result["observation"],
            observation=result["observation"],
            interpretation=result["interpretation"],
            opportunity=result["opportunity"],
            risk=result["risk"],
            recommendation=result["recommendation"],
            impact_score=priority_score,
            relevance_score=relevance_score,
            confidence_score=confidence_score,
            priority=priority,
            status="PENDING_REVIEW",
            evidence=evidence,
            prompt_version=result.get(
                "prompt_version",
                "unknown",
            ),
        )

        db.add(insight)
        db.commit()
        db.refresh(insight)

    except Exception as exc:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail="Failed to persist generated insight.",
        ) from exc

    return InsightResponse(
        insight_id=insight_id,
        brand_id=request.brand_id,
        brand_name=brand.get(
            "name",
            request.brand_id,
        ),
        observation=result["observation"],
        interpretation=result["interpretation"],
        opportunity=result["opportunity"],
        risk=result["risk"],
        recommendation=result["recommendation"],
        relevance_score=relevance_score,
        confidence_score=confidence_score,
        priority_score=priority_score,
        priority=priority,
        evidence_count=int(
            result.get(
                "evidence_count",
                len(evidence),
            )
        ),
        grounded=bool(
            result.get("grounded", False)
        ),
        prompt_version=result.get(
            "prompt_version",
            "unknown",
        ),
        evidence=evidence,
    )