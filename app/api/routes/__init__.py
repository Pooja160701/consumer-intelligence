from uuid import uuid4
from hashlib import sha256
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.dependencies import (
    get_brand_registry,
    get_workflow,
)
from app.api.routes.reviews import router as reviews_router
from app.api.schemas import (
    InsightRequest,
    InsightResponse,
)
from app.models.brand import Brand
from app.models.insight import Insight
from app.models.signal import Signal
from app.models.source import Source
from app.services.database import get_db

router = APIRouter(
    prefix="/api/v1",
    tags=["intelligence"],
)

router.include_router(
    reviews_router
)

@router.get("/health")
def health() -> dict[str, str]:
    """Health check endpoint."""

    return {
        "status": "ok",
    }

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
    """
    Generate an evidence-grounded brand insight.

    Flow:
        1. Resolve brand.
        2. Resolve or persist the incoming signal.
        3. Run intelligence workflow.
        4. Persist generated insight.
        5. Return structured intelligence.
    """

    try:
        brand = brand_registry.get_brand(
            request.brand_id
        )

    except KeyError as exc:
        raise HTTPException(
            status_code=404,
            detail=(
                f"Unknown brand: "
                f"{request.brand_id}"
            ),
        ) from exc

    db_brand = db.get(
        Brand,
        request.brand_id,
    )

    if db_brand is None:
        db_brand = Brand(
            id=brand["id"],
            name=brand["name"],
            category=brand.get(
                "category",
                "general",
            ),
            description=brand.get(
                "description",
            ),
            configuration=brand.get(
                "configuration",
                {},
            ),
        )

        db.add(db_brand)
        db.flush()

    signal_data = request.signal.model_dump()

    metadata = signal_data.get(
        "metadata",
        {},
    )

    signal_id = metadata.get(
        "signal_id"
    )

    try:
        if signal_id:
            signal = db.get(
                Signal,
                signal_id,
            )

            if signal is None:
                raise HTTPException(
                    status_code=404,
                    detail=(
                        f"Signal not found: "
                        f"{signal_id}"
                    ),
                )

        else:
            signal_text = signal_data.get(
                "text",
                "",
            )

            signal_title = signal_data.get(
                "title",
                "Consumer signal",
            )

            source_value = metadata.get(
                "source",
                "dashboard",
            )

            region = metadata.get(
                "region",
                "unknown",
            )

            content_hash = sha256(
                (
                    f"{signal_title}|"
                    f"{signal_text}|"
                    f"{source_value}|"
                    f"{region}"
                ).encode("utf-8")
            ).hexdigest()

            source_id = (
                f"api_source_"
                f"{content_hash[:32]}"
            )

            signal_id = (
                f"api_signal_"
                f"{content_hash[:32]}"
            )

            source = db.get(
                Source,
                source_id,
            )

            if source is None:
                source = Source(
                    id=source_id,
                    source_type=str(
                        source_value
                    ),
                    url=None,
                    title=signal_title,
                    content_hash=content_hash,
                )

                db.add(source)
                db.flush()

            signal = db.get(
                Signal,
                signal_id,
            )

            if signal is None:
                signal = Signal(
                    id=signal_id,
                    source_id=source_id,
                    signal_type=signal_data.get(
                        "signal_type",
                        "consumer_trend",
                    ),
                    category=signal_data.get(
                        "category",
                        "general",
                    ),
                    title=signal_title,
                    text=signal_text,
                    metadata_json=metadata,
                    confidence=1.0,
                )

                db.add(signal)
                db.flush()

    except HTTPException:
        db.rollback()
        raise

    except Exception as exc:
        db.rollback()

        print(
            "INSIGHT WORKFLOW ERROR:",
            repr(exc),
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "Failed to generate intelligence insight."
            ),
        ) from exc

    try:
        signal_data["metadata"] = {
            **signal_data.get("metadata", {}),
            "signal_id": signal_id,
        }

        result = workflow.run(
            signal=signal_data,
            brand=brand,
        )

    except Exception as exc:
        db.rollback()

        print(
            "INSIGHT WORKFLOW ERROR:",
            repr(exc),
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "Failed to generate intelligence insight."
            ),
        ) from exc

    relevance = result.get(
        "relevance",
        {},
    )

    evidence = result.get(
        "evidence",
        [],
    )

    relevance_score = float(
        relevance.get(
            "overall_score",
            0.0,
        )
    )

    confidence_score = float(
        result.get(
            "confidence_score",
            0.0,
        )
    )

    priority_score = float(
        result.get(
            "priority_score",
            0.0,
        )
    )

    priority = result.get(
        "priority",
        "P4",
    )

    prompt_version = result.get(
        "prompt_version",
        "unknown",
    )

    insight_id = (
        f"insight_{uuid4().hex}"
    )

    try:
        insight = Insight(
            id=insight_id,
            brand_id=brand["id"],
            signal_id=signal_id,
            summary=result["observation"],
            observation=result["observation"],
            interpretation=result[
                "interpretation"
            ],
            opportunity=result[
                "opportunity"
            ],
            risk=result["risk"],
            recommendation=result[
                "recommendation"
            ],
            impact_score=priority_score,
            relevance_score=relevance_score,
            confidence_score=confidence_score,
            priority=priority,
            status="PENDING_REVIEW",
            evidence=evidence,
            prompt_version=prompt_version,
        )

        db.add(insight)
        db.commit()
        db.refresh(insight)

    except Exception as exc:
        db.rollback()

        print(
            "INSIGHT WORKFLOW ERROR:",
            repr(exc),
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "Failed to generate intelligence insight."
            ),
        ) from exc

    return InsightResponse(
        insight_id=insight_id,

        brand_id=request.brand_id,

        brand_name=brand.get(
            "name",
            request.brand_id,
        ),

        observation=result[
            "observation"
        ],

        interpretation=result[
            "interpretation"
        ],

        opportunity=result[
            "opportunity"
        ],

        risk=result[
            "risk"
        ],

        recommendation=result[
            "recommendation"
        ],

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
            result.get(
                "grounded",
                False,
            )
        ),

        prompt_version=prompt_version,

        evidence=evidence,
    )