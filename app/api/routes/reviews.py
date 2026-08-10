from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.schemas import (
    ReviewRequest,
    ReviewResponse,
)
from app.models.insight import Insight
from app.services.audit import create_review
from app.services.database import get_db

router = APIRouter(
    prefix="/reviews",
    tags=["reviews"],
)

@router.post(
    "",
    response_model=ReviewResponse,
)
def submit_review(
    request: ReviewRequest,
    db: Session = Depends(get_db),
) -> ReviewResponse:
    """
    Submit a human decision against an AI-generated insight.
    """

    insight = db.get(
        Insight,
        request.insight_id,
    )

    if insight is None:
        raise HTTPException(
            status_code=404,
            detail=(
                f"Insight not found: "
                f"{request.insight_id}"
            ),
        )

    try:
        review = create_review(
            db,
            insight_id=request.insight_id,
            reviewer_action=request.reviewer_action,
            comment=request.comment,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    return ReviewResponse(
        id=review.id,
        insight_id=review.insight_id,
        reviewer_action=review.reviewer_action,
        comment=review.comment,
        status="RECORDED",
    )