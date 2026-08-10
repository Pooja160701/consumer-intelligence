import json
from typing import Any

class InsightParser:
    """Parse structured insight responses from an LLM."""

    REQUIRED_FIELDS = {
        "observation",
        "interpretation",
        "opportunity",
        "risk",
        "recommendation",
    }

    def parse(
        self,
        response: str,
    ) -> dict[str, Any]:
        """
        Parse a JSON insight response.

        Raises ValueError when required fields are missing.
        """

        try:
            data = json.loads(response)
        except json.JSONDecodeError as exc:
            raise ValueError(
                "LLM response is not valid JSON."
            ) from exc

        if not isinstance(data, dict):
            raise ValueError(
                "LLM response must be a JSON object."
            )

        missing = (
            self.REQUIRED_FIELDS
            - data.keys()
        )

        if missing:
            raise ValueError(
                "LLM response missing required fields: "
                + ", ".join(sorted(missing))
            )

        return data