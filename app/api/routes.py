from fastapi import APIRouter, HTTPException
from app.api.schemas import (
    InsightRequest,
    InsightResponse,
)
from app.api.dependencies import get_workflow

router = APIRouter(
    prefix="/api/v1",
    tags=["intelligence"],
)

@router.get("/health")
def health() -> dict[str, str]:
    return {
        "status": "ok",
    }

@router.post(
    "/insights",
    response_model=InsightResponse,
)
def generate_insight(
    request: InsightRequest,
) -> InsightResponse:
    """
    Generate an evidence-grounded brand insight.
    """

    workflow = get_workflow()

    try:
        result = workflow.run(
            signal=request.signal.model_dump(),
            brand={
                "id": request.brand_id,
                "name": request.brand_id,
                "category": request.signal.category,
                "strategic_priorities": [],
                "keywords": [],
                "target_consumer": [],
                "geography": [],
            },
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc

    relevance = result.get(
        "relevance",
        {},
    )

    evidence = result.get(
        "evidence",
        [],
    )

    return InsightResponse(
        brand_id=request.brand_id,
        brand_name=request.brand_id,

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

        relevance_score=float(
            relevance.get(
                "overall_score",
                0.0,
            )
        ),

        confidence_score=float(
            result.get(
                "confidence_score",
                0.0,
            )
        ),

        priority_score=float(
            result.get(
                "priority_score",
                0.0,
            )
        ),

        priority=result.get(
            "priority",
            "P4",
        ),

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

        prompt_version=result.get(
            "prompt_version",
            "unknown",
        ),

        evidence=evidence,
    )