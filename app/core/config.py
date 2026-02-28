from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    POSTGRES_URL: str
    QDRANT_URL: str
    EMBEDDING_MODEL_NAME: str
    LLM_PROVIDER: str
    LLM_API_KEY: str

    # Phase 4: Retrieval Intelligence Upgrade
    BM25_ENABLED: bool = True
    BM25_WEIGHT: float = 0.3
    VECTOR_WEIGHT: float = 0.7
    RERANKER_ENABLED: bool = False
    RERANKER_MODEL: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"
    CONTEXT_TOKEN_BUDGET: int = 3000
    MIN_RELEVANCE_THRESHOLD: float = 0.1

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()

