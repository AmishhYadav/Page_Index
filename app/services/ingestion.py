from sqlalchemy.orm import Session
from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct
from app.models.document import Document, Page, Section
from app.db.qdrant import get_qdrant_client
from app.services.embeddings import get_embedding_provider
import logging
from typing import List, Dict, Any
import uuid

logger = logging.getLogger(__name__)

class IngestionService:
    def __init__(self, db: Session):
        self.db = db
        self.qdrant_client = get_qdrant_client()
        self.embedding_provider = get_embedding_provider()

    def ingest_document(self, filename: str, pages_data: List[Dict[str, Any]]) -> Document:
        """
        Orchestrates hierarchical ingestion:
        1. Write metadata to PostgreSQL (Doc -> Page -> Section).
        2. Generate embeddings for sections.
        3. Upsert to Qdrant.
        """
        try:
            # 1. Create Document
            db_doc = Document(filename=filename, status="processing")
            self.db.add(db_doc)
            self.db.flush()  # Get doc ID

            sections_to_embed = []
            
            # 2. Extract hierarchy and prepare for Postgres/Qdrant
            for page_entry in pages_data:
                db_page = Page(
                    document_id=db_doc.id,
                    page_number=page_entry["page_number"]
                )
                self.db.add(db_page)
                self.db.flush()  # Get page ID

                for section_entry in page_entry["sections"]:
                    db_section = Section(
                        page_id=db_page.id,
                        title=section_entry["title"],
                        content=section_entry["content"],
                        section_index=section_entry["section_index"]
                    )
                    self.db.add(db_section)
                    self.db.flush() # Get section ID
                    
                    sections_to_embed.append({
                        "id": str(db_section.id),
                        "content": db_section.content,
                        "metadata": {
                            "document_id": str(db_doc.id),
                            "page_number": db_page.page_number,
                            "section_title": db_section.title
                        }
                    })

            # Commit Postgres transaction first
            db_doc.status = "indexed"
            self.db.commit()
            self.db.refresh(db_doc)
            
            logger.info(f"Persisted hierarchy for '{filename}' to PostgreSQL. Total sections: {len(sections_to_embed)}")

            # 3. Generate Embeddings and Sync to Qdrant
            if sections_to_embed:
                texts = [s["content"] for s in sections_to_embed]
                embeddings = self.embedding_provider.embed(texts)
                
                points = []
                for idx, emb in enumerate(embeddings):
                    section_info = sections_to_embed[idx]
                    points.append(PointStruct(
                        id=section_info["id"],
                        vector=emb,
                        payload=section_info["metadata"]
                    ))
                
                self.qdrant_client.upsert(
                    collection_name="sections",
                    points=points
                )
                logger.info(f"Synchronized {len(points)} vectors to Qdrant for document '{filename}'")

            return db_doc

        except Exception as e:
            self.db.rollback()
            logger.error(f"Ingestion failed for document '{filename}': {str(e)}", exc_info=True)
            raise
