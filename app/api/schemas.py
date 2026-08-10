from typing import Any
from pydantic import BaseModel, Field

class SignalRequest(BaseModel):
    title: str = Field(min_length=1)
    text: str = Field(min_length=1)
    category: str = Field(min_length=1)
    signal_type: str = Field(min_length=1)
    metadata: dict[str, Any] = Field(
        default_factory=dict
    )

class InsightRequest(BaseModel):
    signal: SignalRequest
    brand_id: str = Field(min_length=1)

class EvidenceResponse(BaseModel):
    signal_id: str
    title: str
    text: str
    category: str
    source_type: str
    score: float
    metadata: dict[str, Any]

class InsightResponse(BaseModel):
    brand_id: str
    brand_name: str

    observation: str
    interpretation: str
    opportunity: str
    risk: str
    recommendation: str

    relevance_score: float
    confidence_score: float

    priority_score: float
    priority: str

    evidence_count: int
    grounded: bool
    prompt_version: str

    evidence: list[EvidenceResponse]