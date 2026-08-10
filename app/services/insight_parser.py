import json
from typing import Any

class InsightParser:
    """Parse and validate structured insight responses from an LLM."""

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
        Parse and validate a JSON insight response.

        Raises ValueError for malformed or incomplete responses.
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

        for field in self.REQUIRED_FIELDS:
            value = data[field]

            if not isinstance(value, str):
                raise ValueError(
                    f"LLM field '{field}' must be a string."
                )

            if not value.strip():
                raise ValueError(
                    f"LLM field '{field}' cannot be empty."
                )

        return data