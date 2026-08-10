import os
from abc import ABC, abstractmethod
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

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
    Deterministic provider used for tests and CI.

    This provider never calls an external service.
    """

    def generate(
        self,
        prompt: str,
        *,
        system_prompt: str | None = None,
        temperature: float = 0.0,
    ) -> str:
        del prompt
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

class OpenAILLMProvider(LLMProvider):
    """
    Production LLM provider backed by the OpenAI Responses API.

    The API key is read exclusively from OPENAI_API_KEY.
    """

    def __init__(
        self,
        model: str | None = None,
    ) -> None:
        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise RuntimeError(
                "OPENAI_API_KEY is required when using "
                "OpenAILLMProvider."
            )

        self.client = OpenAI(api_key=api_key)

        self.model = (
            model
            or os.getenv(
                "OPENAI_MODEL",
                "gpt-5.5",
            )
        )

    def generate(
        self,
        prompt: str,
        *,
        system_prompt: str | None = None,
        temperature: float = 0.0,
    ) -> str:
        del temperature

        response = self.client.responses.create(
            model=self.model,
            instructions=system_prompt,
            input=prompt,
        )

        return response.output_text

def create_llm_provider() -> LLMProvider:
    """
    Create the configured LLM provider.

    Supported providers:
    - mock
    - openai
    """

    provider = os.getenv(
        "LLM_PROVIDER",
        "mock",
    ).lower()

    if provider == "openai":
        return OpenAILLMProvider()

    if provider == "mock":
        return MockLLMProvider()

    raise ValueError(
        f"Unsupported LLM_PROVIDER: {provider}"
    )