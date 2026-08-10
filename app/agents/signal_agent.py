from typing import Any

class SignalAnalysisAgent:
    """Analyze the incoming signal before downstream reasoning."""

    def run(
        self,
        signal: dict[str, Any],
    ) -> dict[str, Any]:
        title = str(
            signal.get("title", "")
        ).strip()

        text = str(
            signal.get("text", "")
        ).strip()

        observation = (
            f"{title}. {text}"
            if text
            else title
        )

        return {
            "observation": observation,
        }