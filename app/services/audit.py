from datetime import datetime, timezone
from uuid import uuid4
from sqlalchemy.orm import Session
from app.models.review import HumanReview

ALLOWED_REVIEW_ACTIONS = {
    "APPROVE",
    "REJECT",
    "MODIFY",
}

def create_review(
    db: Session,
    *,
    insight_id: str,
    reviewer_action: str,
    comment: str | None = None,
) -> HumanReview:
    """
    Persist a human review decision for an insight.
    """

    action = reviewer_action.upper()

    if action not in ALLOWED_REVIEW_ACTIONS:
        raise ValueError(
            f"Unsupported reviewer action: {reviewer_action}"
        )

    review = HumanReview(
        id=f"review_{uuid4().hex}",
        insight_id=insight_id,
        reviewer_action=action,
        comment=comment,
        created_at=datetime.now(timezone.utc),
    )

    db.add(review)
    db.commit()
    db.refresh(review)

    return review