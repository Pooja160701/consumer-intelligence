from functools import lru_cache
from sentence_transformers import SentenceTransformer
from app.config.settings import settings

class EmbeddingService:
    """Generate semantic embeddings for intelligence documents."""

    def __init__(
        self,
        model_name: str | None = None,
    ) -> None:
        self.model_name = (
            model_name or settings.embedding_model
        )

        self.model = SentenceTransformer(
            self.model_name
        )

    def embed_texts(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        """Generate embeddings for multiple texts."""

        if not texts:
            return []

        embeddings = self.model.encode(
            texts,
            normalize_embeddings=True,
            show_progress_bar=False,
        )

        return embeddings.tolist()

    def embed_text(
        self,
        text: str,
    ) -> list[float]:
        """Generate an embedding for one text."""

        return self.embed_texts([text])[0]

    @property
    def dimension(self) -> int:
        """Return the embedding dimension."""

        return self.model.get_sentence_embedding_dimension()

@lru_cache(maxsize=1)
def get_embedding_service() -> EmbeddingService:
    """Return a cached embedding service."""

    return EmbeddingService()