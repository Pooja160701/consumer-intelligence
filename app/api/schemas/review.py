from typing import Literal
from pydantic import BaseModel, Field

ReviewerAction = Literal[
    "APPROVE",
    "REJECT",
    "MODIFY",
]

class ReviewRequest(BaseModel):
    insight_id: str = Field(min_length=1)

    reviewer_action: ReviewerAction

    comment: str | None = None

class ReviewResponse(BaseModel):
    id: str
    insight_id: str
    reviewer_action: ReviewerAction
    comment: str | None
    status: str