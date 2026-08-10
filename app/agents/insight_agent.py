from typing import Any
from app.services.insight_generator import InsightGenerator
from app.services.insight_parser import InsightParser
from app.services.llm import LLMProvider, MockLLMProvider

class InsightGenerationAgent:
    """
    Generate structured, evidence-grounded insights.

    The agent delegates model interaction to InsightGenerator,
    keeping the LangGraph layer independent from the concrete
    LLM provider.
    """

    def __init__(
        self,
        llm: LLMProvider | None = None,
        parser: InsightParser | None = None,
    ) -> None:
        self.generator = InsightGenerator(
            llm=llm or MockLLMProvider()
        )

        self.parser = parser or InsightParser()

    def run(
        self,
        signal: dict[str, Any],
        brand: dict[str, Any],
        relevance: dict[str, float],
        evidence: list[dict[str, Any]],
    ) -> dict[str, Any]:
        """Generate and validate a structured insight."""

        generated = self.generator.generate(
            signal=signal,
            brand=brand,
            relevance=relevance,
            evidence=evidence,
        )

        parsed = self.parser.parse(
            generated["raw_response"]
        )

        return {
            **parsed,
            "prompt_version": generated[
                "prompt_version"
            ],
            "evidence_count": generated[
                "evidence_count"
            ],
            "grounded": generated[
                "grounded"
            ],
            "confidence_score": generated[
                "confidence_score"
            ],
        }