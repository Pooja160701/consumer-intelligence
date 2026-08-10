from fastapi import APIRouter, Depends, HTTPException
from app.api.dependencies import (
    get_brand_registry,
    get_workflow,
)
from app.api.schemas import (
    InsightRequest,
    InsightResponse,
)

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
    workflow=Depends(get_workflow),
    brand_registry=Depends(get_brand_registry),
) -> InsightResponse:
    """Generate an evidence-grounded brand insight."""

    try:
        brand = brand_registry.get_brand(
            request.brand_id
        )

    except KeyError as exc:
        raise HTTPException(
            status_code=404,
            detail=f"Unknown brand: {request.brand_id}",
        ) from exc

    try:
        result = workflow.run(
            signal=request.signal.model_dump(),
            brand=brand,
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Failed to generate intelligence insight.",
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
        brand_name=brand.get(
            "name",
            request.brand_id,
        ),

        observation=result["observation"],
        interpretation=result["interpretation"],
        opportunity=result["opportunity"],
        risk=result["risk"],
        recommendation=result["recommendation"],

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