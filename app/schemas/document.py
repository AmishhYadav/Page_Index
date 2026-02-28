from pydantic import BaseModel, UUID4
from typing import List, Optional
from datetime import datetime

class SectionBase(BaseModel):
    title: str
    content: str
    section_index: int

class SectionResponse(SectionBase):
    id: UUID4
    page_id: UUID4

    class Config:
        from_attributes = True

class PageResponse(BaseModel):
    id: UUID4
    document_id: UUID4
    page_number: int
    sections: List[SectionResponse] = []

    class Config:
        from_attributes = True

class DocumentResponse(BaseModel):
    id: UUID4
    filename: str
    status: str
    created_at: datetime
    updated_at: datetime
    pages: List[PageResponse] = []

    class Config:
        from_attributes = True

class IngestionResponse(BaseModel):
    document_id: UUID4
    status: str
    message: str
