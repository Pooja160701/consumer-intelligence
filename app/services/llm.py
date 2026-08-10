from abc import ABC, abstractmethod
from typing import Any

class LLMProvider(ABC):
    """Provider-independent interface for language models."""

    @abstractmethod
    def generate(
        self,
        prompt: str,
        *,
        system_prompt: str | None = None,
        temperature: float = 0.0,
    ) -> str:
        """Generate text from a prompt."""
        raise NotImplementedError

class MockLLMProvider(LLMProvider):
    """
    Deterministic provider used for tests and local development.

    This keeps the application functional without requiring
    an external model or API key.
    """

    def generate(
        self,
        prompt: str,
        *,
        system_prompt: str | None = None,
        temperature: float = 0.0,
    ) -> str:
        del system_prompt
        del temperature

        return (
            "{"
            '"observation": "The supplied signal is relevant '
            'to the selected brand.",'
            '"interpretation": "The retrieved evidence provides '
            'context for evaluating the signal.",'
            '"opportunity": "The brand can evaluate a targeted '
            'response after further validation.",'
            '"risk": "Acting without sufficient validation may '
            'lead to unnecessary investment.",'
            '"recommendation": "Validate the signal with '
            'additional evidence before making a major decision."'
            "}"
        )