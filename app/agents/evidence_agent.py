from typing import Any
from app.services.retrieval import FAISSRetriever

class EvidenceAgent:
    """Retrieve supporting evidence from the semantic index."""

    def __init__(
        self,
        retriever: FAISSRetriever,
        top_k: int = 3,
    ) -> None:
        if top_k < 1:
            raise ValueError(
                "top_k must be greater than zero."
            )

        self.retriever = retriever
        self.top_k = top_k

    def run(
        self,
        signal: dict[str, Any],
    ) -> dict[str, Any]:
        """Retrieve evidence relevant to a signal."""

        query_parts = [
            str(signal.get("title", "")).strip(),
            str(signal.get("text", "")).strip(),
            str(signal.get("category", "")).strip(),
        ]

        query = " ".join(
            part
            for part in query_parts
            if part
        )

        if not query:
            return {
                "evidence": [],
            }

        results = self.retriever.search(
            query,
            top_k=self.top_k,
        )

        evidence = [
            {
                "signal_id": result.signal_id,
                "title": result.title,
                "text": result.text,
                "category": result.category,
                "source_type": result.source_type,
                "score": result.score,
                "metadata": result.metadata,
            }
            for result in results
        ]

        return {
            "evidence": evidence,
        }