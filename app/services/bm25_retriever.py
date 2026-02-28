"""
BM25-like keyword retriever using PostgreSQL tsvector/tsquery full-text search.
Returns ranked section IDs with scores for fusion with vector search results.
"""
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List, Tuple
import logging

logger = logging.getLogger(__name__)


class BM25Retriever:
    """
    PostgreSQL full-text search retriever.
    Uses ts_rank_cd for BM25-like scoring against the sections.search_vector column.
    """

    def __init__(self, db: Session):
        self.db = db

    def search(self, query: str, top_k: int = 20) -> List[Tuple[str, float]]:
        """
        Perform keyword-based search using PostgreSQL full-text search.

        Args:
            query: The user's search query.
            top_k: Number of top results to return.

        Returns:
            List of (section_id_str, score) tuples, ordered by relevance.
        """
        if not query.strip():
            return []

        # Use plainto_tsquery for natural language input (handles stopwords, stemming)
        sql = text("""
            SELECT
                s.id::text AS section_id,
                ts_rank_cd(s.search_vector, plainto_tsquery('english', :query)) AS rank
            FROM sections s
            WHERE s.search_vector @@ plainto_tsquery('english', :query)
            ORDER BY rank DESC
            LIMIT :top_k
        """)

        try:
            result = self.db.execute(sql, {"query": query, "top_k": top_k})
            hits = [(row[0], float(row[1])) for row in result]
            logger.info(f"BM25 search returned {len(hits)} results for query: '{query[:50]}...'")
            return hits
        except Exception as e:
            logger.error(f"BM25 search failed: {e}", exc_info=True)
            return []
