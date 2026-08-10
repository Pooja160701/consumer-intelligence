from typing import Any, TypedDict

class IntelligenceState(TypedDict, total=False):
    """Shared state passed between LangGraph nodes."""

    signal: dict[str, Any]

    brand: dict[str, Any]

    relevance: dict[str, float]

    evidence: list[dict[str, Any]]

    observation: str

    interpretation: str

    opportunity: str

    risk: str

    recommendation: str

    prompt_version: str

    evidence_count: int

    grounded: bool

    priority_score: float

    priority: str

    confidence_score: float

    insight: dict[str, Any]

    errors: list[str]