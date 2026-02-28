from pydantic import BaseModel
from typing import List, Optional, Tuple
from uuid import UUID


class RetrievalFilters(BaseModel):
    """Optional filters to scope retrieval."""
    document_ids: Optional[List[UUID]] = None
    filename_contains: Optional[str] = None
    page_range: Optional[Tuple[int, int]] = None  # (min_page, max_page)


class AskRequest(BaseModel):
    query: str
    top_k: int = 5
    filters: Optional[RetrievalFilters] = None


class Citation(BaseModel):
    document_name: str
    page_number: int
    section_title: Optional[str] = None
    text_snippet: str


class AskResponse(BaseModel):
    answer: str
    citations: List[Citation] = []

