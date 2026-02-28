from pydantic import BaseModel
from typing import List, Optional


class AskRequest(BaseModel):
    query: str
    top_k: int = 5


class Citation(BaseModel):
    document_name: str
    page_number: int
    section_title: Optional[str] = None
    text_snippet: str


class AskResponse(BaseModel):
    answer: str
    citations: List[Citation] = []
