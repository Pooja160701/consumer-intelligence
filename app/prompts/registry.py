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
                    "Relevance Scores:\n"
                    "{relevance}\n\n"
                    "Retrieved Evidence:\n"
                    "{evidence}\n\n"
                    "IMPORTANT RULES:\n"
                    "1. Use only the supplied signal and evidence.\n"
                    "2. Do not invent statistics, sources, trends, or facts.\n"
                    "3. Clearly distinguish observation from interpretation.\n"
                    "4. If evidence is insufficient, say so.\n"
                    "5. Do not claim that a source says something unless "
                    "that information appears in the supplied evidence.\n\n"
                    "Return ONLY valid JSON with exactly these fields:\n"
                    "{{\n"
                    '  "observation": "...",\n'
                    '  "interpretation": "...",\n'
                    '  "opportunity": "...",\n'
                    '  "risk": "...",\n'
                    '  "recommendation": "..."\n'
                    "}}"
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