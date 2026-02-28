from sqlalchemy.orm import Session
from sqlalchemy import text
from qdrant_client.http.models import Filter
from app.db.qdrant import get_qdrant_client
from app.services.embeddings import get_embedding_provider
from app.services.bm25_retriever import BM25Retriever
from app.services.fusion import rrf_fuse
from app.models.document import Document, Page, Section
from app.core.config import settings
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class RetrievalResult:
    """Structured result from hierarchical retrieval."""
    def __init__(
        self,
        section_id: str,
        section_title: Optional[str],
        section_content: str,
        section_index: int,
        page_number: int,
        document_filename: str,
        document_id: str,
        score: float,
    ):
        self.section_id = section_id
        self.section_title = section_title
        self.section_content = section_content
        self.section_index = section_index
        self.page_number = page_number
        self.document_filename = document_filename
        self.document_id = document_id
        self.score = score

    def to_dict(self) -> Dict[str, Any]:
        return {
            "section_id": self.section_id,
            "section_title": self.section_title,
            "section_content": self.section_content,
            "section_index": self.section_index,
            "page_number": self.page_number,
            "document_filename": self.document_filename,
            "document_id": self.document_id,
            "score": self.score,
        }


class RetrievalService:
    """
    Orchestrates hybrid hierarchical search:
    1. Dense: Embed query → Qdrant similarity search → top-K Section UUIDs
    2. Sparse: BM25 keyword search via PostgreSQL tsvector
    3. Fuse both signals via Reciprocal Rank Fusion (RRF)
    4. Fetch canonical Section → Page → Document hierarchy from PostgreSQL
    5. Return structured results with full metadata for citation
    """

    def __init__(self, db: Session):
        self.db = db
        self.qdrant_client = get_qdrant_client()
        self.embedding_provider = get_embedding_provider()
        self.bm25_retriever = BM25Retriever(db)

    def _vector_search(self, query: str, top_k: int) -> List[tuple]:
        """Dense vector search via Qdrant."""
        query_vector = self.embedding_provider.embed([query])[0]
        logger.info(f"Embedded query, searching Qdrant for top-{top_k} sections")

        qdrant_response = self.qdrant_client.query_points(
            collection_name="sections",
            query=query_vector,
            limit=top_k,
        )

        qdrant_hits = qdrant_response.points if qdrant_response else []
        return [(str(hit.id), hit.score) for hit in qdrant_hits]

    def search(self, query: str, top_k: int = 5) -> List[RetrievalResult]:
        """
        Perform hybrid hierarchical search (vector + BM25).

        Args:
            query: The user's search query.
            top_k: Number of top results to return.

        Returns:
            List of RetrievalResult objects with full hierarchy context.
        """
        # 1. Dense vector search (always runs)
        vector_results = self._vector_search(query, top_k=top_k * 2)

        # 2. Sparse BM25 search (if enabled)
        bm25_results = []
        if settings.BM25_ENABLED:
            bm25_results = self.bm25_retriever.search(query, top_k=top_k * 2)
            logger.info(f"BM25 returned {len(bm25_results)} results")

        # 3. Fuse results via RRF
        if bm25_results:
            fused = rrf_fuse(
                vector_results,
                bm25_results,
                weights=[settings.VECTOR_WEIGHT, settings.BM25_WEIGHT],
            )
        else:
            # Fallback to vector-only ranking
            fused = vector_results

        # Take top_k from fused list
        fused_top = fused[:top_k]
        if not fused_top:
            logger.info("No results found from any retrieval signal")
            return []

        # Build score map from fused results
        hit_map = {sid: score for sid, score in fused_top}
        section_ids = [sid for sid, _ in fused_top]
        logger.info(f"Fused retrieval produced {len(section_ids)} candidates, fetching hierarchy from Postgres")

        # 4. Fetch canonical hierarchy from PostgreSQL
        rows = (
            self.db.query(Section, Page, Document)
            .join(Page, Section.page_id == Page.id)
            .join(Document, Page.document_id == Document.id)
            .filter(Section.id.in_(section_ids))
            .all()
        )

        # Build results, preserving fused ranking order
        results_map: Dict[str, RetrievalResult] = {}
        for section, page, document in rows:
            section_id_str = str(section.id)
            results_map[section_id_str] = RetrievalResult(
                section_id=section_id_str,
                section_title=section.title,
                section_content=section.content,
                section_index=section.section_index,
                page_number=page.page_number,
                document_filename=document.filename,
                document_id=str(document.id),
                score=hit_map.get(section_id_str, 0.0),
            )

        # Handle orphaned IDs
        for sid in section_ids:
            if sid not in results_map:
                logger.warning(f"Section {sid} found in retrieval but missing from Postgres — skipping")

        # Return in fused ranking order
        ordered_results = [results_map[sid] for sid in section_ids if sid in results_map]
        logger.info(f"Returning {len(ordered_results)} hierarchical results (hybrid retrieval)")
        return ordered_results
