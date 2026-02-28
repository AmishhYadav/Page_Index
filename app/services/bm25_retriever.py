"""
BM25-like keyword retriever using PostgreSQL tsvector/tsquery full-text search.
Returns ranked section IDs with scores for fusion with vector search results.
Supports metadata filters for scoped search.
"""
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List, Tuple, Optional
import logging

logger = logging.getLogger(__name__)


class BM25Retriever:
    """
    PostgreSQL full-text search retriever.
    Uses ts_rank_cd for BM25-like scoring against the sections.search_vector column.
    Supports metadata filtering via document_ids, page_range, and filename.
    """

    def __init__(self, db: Session):
        self.db = db

    def search(self, query: str, top_k: int = 20, filters=None) -> List[Tuple[str, float]]:
        """
        Perform keyword-based search using PostgreSQL full-text search.

        Args:
            query: The user's search query.
            top_k: Number of top results to return.
            filters: Optional RetrievalFilters for scoped search.

        Returns:
            List of (section_id_str, score) tuples, ordered by relevance.
        """
        if not query.strip():
            return []

        # Build dynamic SQL with optional filter clauses
        where_clauses = ["s.search_vector @@ plainto_tsquery('english', :query)"]
        params = {"query": query, "top_k": top_k}

        joins = ""

        if filters:
            if filters.document_ids or filters.filename_contains or filters.page_range:
                joins = " JOIN pages p ON s.page_id = p.id JOIN documents d ON p.document_id = d.id"

            if filters.document_ids:
                doc_ids = [str(d) for d in filters.document_ids]
                where_clauses.append("d.id::text = ANY(:doc_ids)")
                params["doc_ids"] = doc_ids

            if filters.filename_contains:
                where_clauses.append("d.filename ILIKE :fname")
                params["fname"] = f"%{filters.filename_contains}%"

            if filters.page_range:
                min_page, max_page = filters.page_range
                where_clauses.append("p.page_number >= :min_page AND p.page_number <= :max_page")
                params["min_page"] = min_page
                params["max_page"] = max_page

        where_str = " AND ".join(where_clauses)

        sql = text(f"""
            SELECT
                s.id::text AS section_id,
                ts_rank_cd(s.search_vector, plainto_tsquery('english', :query)) AS rank
            FROM sections s{joins}
            WHERE {where_str}
            ORDER BY rank DESC
            LIMIT :top_k
        """)

        try:
            result = self.db.execute(sql, params)
            hits = [(row[0], float(row[1])) for row in result]
            logger.info(f"BM25 search returned {len(hits)} results for query: '{query[:50]}...'")
            return hits
        except Exception as e:
            logger.error(f"BM25 search failed: {e}", exc_info=True)
            return []
