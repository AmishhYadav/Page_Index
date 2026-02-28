from abc import ABC, abstractmethod
from typing import List
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class EmbeddingProvider(ABC):
    @abstractmethod
    def get_dimension(self) -> int:
        pass

    @abstractmethod
    def embed(self, texts: List[str]) -> List[List[float]]:
        pass

class MockEmbeddingProvider(EmbeddingProvider):
    """
    A temporary mock provider for development until a real API is connected.
    It returns deterministic mock vectors based on text length.
    """
    def __init__(self, dimension: int = 384):
        self.dimension = dimension
        logger.info(f"Initialized MockEmbeddingProvider with dimension: {self.dimension}")

    def get_dimension(self) -> int:
        return self.dimension

    def embed(self, texts: List[str]) -> List[List[float]]:
        # Simulate an embedding that returns vectors of length `self.dimension`
        embeddings = []
        for text in texts:
            # Deterministic pseudo-random generation based on text hash for variety
            base_val = hash(text) % 100 / 100.0
            vector = [base_val] * self.dimension
            embeddings.append(vector)
        return embeddings

def get_embedding_provider() -> EmbeddingProvider:
    # Later: Use settings.EMBEDDING_MODEL_NAME to dispatch real providers
    return MockEmbeddingProvider()
