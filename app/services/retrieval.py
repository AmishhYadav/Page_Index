from sqlalchemy.orm import Session
from qdrant_client.http.models import Filter
from app.db.qdrant import get_qdrant_client
from app.services.embeddings import get_embedding_provider
from app.models.document import Document, Page, Section
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
    Orchestrates hierarchical semantic search:
    1. Embed query → Qdrant similarity search → top-K Section UUIDs
    2. Fetch canonical Section → Page → Document hierarchy from PostgreSQL
    3. Return structured results with full metadata for citation
    """

    def __init__(self, db: Session):
        self.db = db
        self.qdrant_client = get_qdrant_client()
        self.embedding_provider = get_embedding_provider()

    def search(self, query: str, top_k: int = 5) -> List[RetrievalResult]:
        """
        Perform hierarchical semantic search.

        Args:
            query: The user's search query.
            top_k: Number of top results to return.

        Returns:
            List of RetrievalResult objects with full hierarchy context.
        """
        # 1. Embed the query
        query_vector = self.embedding_provider.embed([query])[0]
        logger.info(f"Embedded query, searching Qdrant for top-{top_k} sections")

        # 2. Search Qdrant for similar section vectors
        qdrant_response = self.qdrant_client.query_points(
            collection_name="sections",
            query=query_vector,
            limit=top_k,
        )

        qdrant_hits = qdrant_response.points if qdrant_response else []

        if not qdrant_hits:
            logger.info("No results found in Qdrant")
            return []

        # 3. Extract Section UUIDs from Qdrant results
        hit_map = {}  # section_uuid_str -> score
        for hit in qdrant_hits:
            hit_map[str(hit.id)] = hit.score

        section_ids = list(hit_map.keys())
        logger.info(f"Qdrant returned {len(section_ids)} hits, fetching hierarchy from Postgres")

        # 4. Fetch canonical hierarchy from PostgreSQL
        # Join Section → Page → Document in a single query
        rows = (
            self.db.query(Section, Page, Document)
            .join(Page, Section.page_id == Page.id)
            .join(Document, Page.document_id == Document.id)
            .filter(Section.id.in_(section_ids))
            .all()
        )

        # Build results, preserving Qdrant ranking order
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

        # Handle orphaned Qdrant IDs (exist in vector store but not in Postgres)
        for sid in section_ids:
            if sid not in results_map:
                logger.warning(f"Section {sid} found in Qdrant but missing from Postgres — skipping")

        # Return results in original Qdrant ranking order
        ordered_results = []
        for sid in section_ids:
            if sid in results_map:
                ordered_results.append(results_map[sid])

        logger.info(f"Returning {len(ordered_results)} hierarchical results")
        return ordered_results
