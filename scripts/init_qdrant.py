import os
import sys
from qdrant_client.http.models import Distance, VectorParams

# Add the root directory to the sys.path
sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), '..')))

from app.db.qdrant import get_qdrant_client
from app.services.embeddings import get_embedding_provider
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_collections():
    client = get_qdrant_client()
    provider = get_embedding_provider()
    dimension = provider.get_dimension()
    collection_name = "sections"
    
    logger.info(f"Initializing Qdrant collection '{collection_name}' with dimension {dimension}")
    
    if client.collection_exists(collection_name=collection_name):
        logger.info(f"Collection '{collection_name}' already exists.")
    else:
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=dimension, distance=Distance.COSINE),
        )
        logger.info(f"Successfully created collection '{collection_name}'.")

if __name__ == "__main__":
    init_collections()
