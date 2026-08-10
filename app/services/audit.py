from datetime import datetime, timezone
from uuid import uuid4
from sqlalchemy.orm import Session
from app.models.insight import Insight
from app.models.review import HumanReview

ALLOWED_REVIEW_ACTIONS = {
    "APPROVE",
    "REJECT",
    "MODIFY",
}

REVIEW_STATUS_MAP = {
    "APPROVE": "APPROVED",
    "REJECT": "REJECTED",
    "MODIFY": "NEEDS_MODIFICATION",
}

def create_review(
    db: Session,
    *,
    insight_id: str,
    reviewer_action: str,
    comment: str | None = None,
) -> HumanReview:
    """
    Persist a human review decision and update the
    lifecycle status of the associated insight.
    """

    action = reviewer_action.upper()

    if action not in ALLOWED_REVIEW_ACTIONS:
        raise ValueError(
            f"Unsupported reviewer action: {reviewer_action}"
        )

    insight = db.get(
        Insight,
        insight_id,
    )

    if insight is None:
        raise ValueError(
            f"Insight not found: {insight_id}"
        )

    review = HumanReview(
        id=f"review_{uuid4().hex}",
        insight_id=insight_id,
        reviewer_action=action,
        comment=comment,
        created_at=datetime.now(timezone.utc),
    )

    insight.status = REVIEW_STATUS_MAP[action]

    db.add(review)

    try:
        db.commit()
        db.refresh(review)
    except Exception:
        db.rollback()
        raise

    return review