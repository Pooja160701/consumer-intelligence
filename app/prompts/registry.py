from dataclasses import dataclass

@dataclass(frozen=True)
class PromptTemplate:
    """Versioned prompt template."""

    name: str
    version: str
    template: str

class PromptRegistry:
    """Central registry for versioned intelligence prompts."""

    def __init__(self) -> None:
        self._prompts: dict[str, PromptTemplate] = {}

        self.register(
            PromptTemplate(
                name="insight_generation",
                version="v1",
                template=(
                    "Analyze the following consumer intelligence signal "
                    "for the selected brand.\n\n"
                    "Brand:\n"
                    "{brand_name}\n\n"
                    "Signal:\n"
                    "{signal_text}\n\n"
                    "Relevance:\n"
                    "{relevance}\n\n"
                    "Evidence:\n"
                    "{evidence}\n\n"
                    "Return a concise business insight covering:\n"
                    "1. Observation\n"
                    "2. Interpretation\n"
                    "3. Opportunity\n"
                    "4. Risk\n"
                    "5. Recommendation"
                ),
            )
        )

        self.register(
            PromptTemplate(
                name="signal_summary",
                version="v1",
                template=(
                    "Summarize this consumer intelligence signal "
                    "without inventing facts.\n\n"
                    "Signal:\n"
                    "{signal_text}\n\n"
                    "Return:\n"
                    "- What happened\n"
                    "- Why it matters\n"
                    "- Evidence strength"
                ),
            )
        )

        self.register(
            PromptTemplate(
                name="recommendation",
                version="v1",
                template=(
                    "Generate a business recommendation using only "
                    "the supplied signal, brand context, and evidence.\n\n"
                    "Brand:\n"
                    "{brand_name}\n\n"
                    "Signal:\n"
                    "{signal_text}\n\n"
                    "Evidence:\n"
                    "{evidence}\n\n"
                    "Do not invent supporting evidence."
                ),
            )
        )

    def register(
        self,
        prompt: PromptTemplate,
    ) -> None:
        key = self._key(
            prompt.name,
            prompt.version,
        )

        self._prompts[key] = prompt

    def get(
        self,
        name: str,
        version: str = "v1",
    ) -> PromptTemplate:
        key = self._key(
            name,
            version,
        )

        if key not in self._prompts:
            raise KeyError(
                f"Prompt not found: {name}:{version}"
            )

        return self._prompts[key]

    def render(
        self,
        name: str,
        version: str = "v1",
        **kwargs: object,
    ) -> str:
        prompt = self.get(
            name,
            version,
        )

        return prompt.template.format(
            **kwargs
        )

    @staticmethod
    def _key(
        name: str,
        version: str,
    ) -> str:
        return f"{name}:{version}"