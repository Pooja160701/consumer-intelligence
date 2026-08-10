from dataclasses import dataclass
from typing import Any
import faiss
import numpy as np
from app.services.embeddings import EmbeddingService

@dataclass
class RetrievedEvidence:
    """Evidence returned by semantic retrieval."""

    signal_id: str
    title: str
    text: str
    category: str
    source_type: str
    score: float
    metadata: dict[str, Any]

class FAISSRetriever:
    """
    Lightweight semantic retrieval layer.

    FAISS is used as the POC vector index while PostgreSQL
    remains the system of record.
    """

    def __init__(
        self,
        embedding_service: EmbeddingService,
    ) -> None:
        self.embedding_service = embedding_service

        self.index: faiss.Index | None = None

        self.documents: list[dict[str, Any]] = []

    def build_index(
        self,
        signals: list[dict[str, Any]],
    ) -> None:
        """Build a FAISS index from signal documents."""

        if not signals:
            self.index = None
            self.documents = []
            return

        texts = [
            self._document_text(signal)
            for signal in signals
        ]

        embeddings = self.embedding_service.embed_texts(
            texts
        )

        matrix = np.asarray(
            embeddings,
            dtype="float32",
        )

        dimension = matrix.shape[1]

        index = faiss.IndexFlatIP(dimension)

        index.add(matrix)

        self.index = index
        self.documents = signals.copy()

    def search(
        self,
        query: str,
        top_k: int = 5,
    ) -> list[RetrievedEvidence]:
        """Return the most semantically relevant signals."""

        if self.index is None or not self.documents:
            return []

        query_embedding = self.embedding_service.embed_text(
            query
        )

        query_vector = np.asarray(
            [query_embedding],
            dtype="float32",
        )

        limit = min(
            top_k,
            len(self.documents),
        )

        scores, indices = self.index.search(
            query_vector,
            limit,
        )

        results: list[RetrievedEvidence] = []

        for score, index in zip(
            scores[0],
            indices[0],
        ):
            if index < 0:
                continue

            document = self.documents[index]

            results.append(
                RetrievedEvidence(
                    signal_id=document["id"],
                    title=document["title"],
                    text=document["text"],
                    category=document["category"],
                    source_type=document["source_type"],
                    score=float(score),
                    metadata=document.get(
                        "metadata",
                        {},
                    ),
                )
            )

        return results

    @staticmethod
    def _document_text(
        signal: dict[str, Any],
    ) -> str:
        """Create searchable text from a signal."""

        return " ".join(
            [
                signal.get("title", ""),
                signal.get("text", ""),
                signal.get("category", ""),
                signal.get("signal_type", ""),
            ]
        )