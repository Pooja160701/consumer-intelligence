from typing import Any

class InsightGenerationAgent:
    """
    Convert signal + brand context + evidence
    into a structured business insight.
    """

    def run(
        self,
        signal: dict[str, Any],
        brand: dict[str, Any],
        relevance: dict[str, float],
        evidence: list[dict[str, Any]],
    ) -> dict[str, Any]:
        brand_name = brand["name"]
        signal_title = signal["title"]

        relevance_score = relevance.get(
            "overall_score",
            0.0,
        )

        observation = (
            f"{signal_title} is relevant to "
            f"{brand_name} with a relevance score of "
            f"{relevance_score:.2f}."
        )

        if evidence:
            interpretation = (
                f"The signal is supported by "
                f"{len(evidence)} retrieved evidence item(s) "
                f"from the intelligence corpus."
            )
        else:
            interpretation = (
                "No supporting evidence was retrieved "
                "from the current intelligence corpus."
            )

        if relevance_score >= 0.70:
            opportunity = (
                f"{brand_name} could evaluate a targeted "
                "response aligned with the observed trend."
            )

            risk = (
                "Competitors may capture consumer demand "
                "if the trend becomes sustained."
            )

            recommendation = (
                "Validate the trend with additional consumer "
                "evidence and assess a focused product, "
                "positioning, or campaign response."
            )

        elif relevance_score >= 0.40:
            opportunity = (
                f"{brand_name} should monitor the signal "
                "for stronger evidence of sustained demand."
            )

            risk = (
                "Acting too early could create unnecessary "
                "investment before the trend is validated."
            )

            recommendation = (
                "Continue monitoring and gather additional "
                "evidence before committing resources."
            )

        else:
            opportunity = (
                "Limited immediate opportunity identified."
            )

            risk = (
                "Low relevance means immediate action may "
                "not be justified."
            )

            recommendation = (
                "Keep the signal in the intelligence backlog "
                "and reassess if relevance increases."
            )

        confidence = self._confidence(
            relevance_score,
            evidence,
        )

        return {
            "observation": observation,
            "interpretation": interpretation,
            "opportunity": opportunity,
            "risk": risk,
            "recommendation": recommendation,
            "confidence_score": confidence,
        }

    @staticmethod
    def _confidence(
        relevance_score: float,
        evidence: list[dict[str, Any]],
    ) -> float:
        evidence_score = 0.0

        if evidence:
            evidence_score = min(
                max(
                    float(
                        evidence[0].get(
                            "score",
                            0.0,
                        )
                    ),
                    0.0,
                ),
                1.0,
            )

        confidence = (
            relevance_score * 0.60
            + evidence_score * 0.40
        )

        return round(
            min(confidence, 1.0),
            4,
        )