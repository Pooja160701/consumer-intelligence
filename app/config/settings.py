from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    app_name: str = "Think9 Consumer Intelligence OS"
    app_env: str = "development"
    debug: bool = True

    api_host: str = "0.0.0.0"  # nosec B104
    api_port: int = 8000

    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_db: str = "think9_intelligence"
    postgres_user: str = "think9"
    postgres_password: str = "think9_dev_password"

    database_url: str = (
        "postgresql+psycopg://"
        "think9:think9_dev_password"
        "@localhost:5432/"
        "think9_intelligence"
    )

    llm_provider: str = "mock"
    llm_model: str = "mock-model"

    embedding_provider: str = "sentence-transformers"
    embedding_model: str = "all-MiniLM-L6-v2"

    vector_store: str = "faiss"
    retrieval_top_k: int = 5

    api_key_required: bool = False

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

@lru_cache
def get_settings() -> Settings:
    """Return a cached application settings instance."""
    return Settings()

settings = get_settings()