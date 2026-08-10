import json
from typing import Any
from app.prompts.registry import PromptRegistry
from app.services.llm import LLMProvider

class InsightGenerator:
    """
    Generate evidence-grounded business insights.

    The generator is independent of the concrete LLM provider.
    """

    def __init__(
        self,
        llm: LLMProvider,
        prompt_registry: PromptRegistry | None = None,
    ) -> None:
        self.llm = llm
        self.prompts = (
            prompt_registry
            or PromptRegistry()
        )

    def generate(
        self,
        signal: dict[str, Any],
        brand: dict[str, Any],
        relevance: dict[str, float],
        evidence: list[dict[str, Any]],
    ) -> dict[str, Any]:
        """
        Generate a structured insight from supplied evidence.
        """

        evidence_context = self._format_evidence(
            evidence
        )

        prompt = self.prompts.render(
            "insight_generation",
            "v1",
            brand_name=brand["name"],
            signal_text=self._format_signal(signal),
            relevance=json.dumps(
                relevance,
                indent=2,
            ),
            evidence=evidence_context,
        )

        raw_response = self.llm.generate(
            prompt,
            system_prompt=(
                "You are a consumer intelligence analyst. "
                "Use only the supplied signal and evidence. "
                "Do not invent market facts, statistics, "
                "sources, or consumer behavior."
            ),
            temperature=0.0,
        )

        return {
            "raw_response": raw_response,
            "prompt_version": "insight_generation:v1",
            "evidence_count": len(evidence),
            "grounded": bool(evidence),
        }

    @staticmethod
    def _format_signal(
        signal: dict[str, Any],
    ) -> str:
        return (
            f"Title: {signal.get('title', '')}\n"
            f"Text: {signal.get('text', '')}\n"
            f"Category: {signal.get('category', '')}\n"
            f"Type: {signal.get('signal_type', '')}"
        )

    @staticmethod
    def _format_evidence(
        evidence: list[dict[str, Any]],
    ) -> str:
        if not evidence:
            return (
                "NO RETRIEVED EVIDENCE. "
                "Do not make unsupported factual claims."
            )

        formatted: list[str] = []

        for index, item in enumerate(
            evidence,
            start=1,
        ):
            formatted.append(
                (
                    f"[Evidence {index}]\n"
                    f"Signal ID: {item.get('signal_id', '')}\n"
                    f"Title: {item.get('title', '')}\n"
                    f"Text: {item.get('text', '')}\n"
                    f"Category: {item.get('category', '')}\n"
                    f"Source Type: {item.get('source_type', '')}\n"
                    f"Retrieval Score: "
                    f"{float(item.get('score', 0.0)):.4f}"
                )
            )

        return "\n\n".join(formatted)