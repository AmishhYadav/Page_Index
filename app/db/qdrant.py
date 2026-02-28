from qdrant_client import QdrantClient
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

# Global client instance to reuse connection pools
client = None

def get_qdrant_client() -> QdrantClient:
    global client
    if client is None:
        logger.info(f"Connecting to Qdrant at {settings.QDRANT_URL}")
        client = QdrantClient(url=settings.QDRANT_URL)
    return client
