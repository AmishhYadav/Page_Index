import uuid
from sqlalchemy import Column, Integer, String, Text, ForeignKey, UniqueConstraint, DateTime, Index
from sqlalchemy.dialects.postgresql import UUID, TSVECTOR
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.models.base import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    filename = Column(String, nullable=False)
    status = Column(String, nullable=False, default="processing")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

    pages = relationship("Page", back_populates="document", cascade="all, delete-orphan", passive_deletes=True)

class Page(Base):
    __tablename__ = "pages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    document_id = Column(UUID(as_uuid=True), ForeignKey("documents.id", ondelete="CASCADE"), nullable=False, index=True)
    page_number = Column(Integer, nullable=False)

    document = relationship("Document", back_populates="pages")
    sections = relationship("Section", back_populates="page", cascade="all, delete-orphan", passive_deletes=True)

    __table_args__ = (
        UniqueConstraint('document_id', 'page_number', name='uq_doc_page'),
    )

class Section(Base):
    __tablename__ = "sections"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    page_id = Column(UUID(as_uuid=True), ForeignKey("pages.id", ondelete="CASCADE"), nullable=False, index=True)
    section_index = Column(Integer, nullable=False)
    title = Column(String, nullable=True)
    content = Column(Text, nullable=False)
    search_vector = Column(TSVECTOR, nullable=True)

    page = relationship("Page", back_populates="sections")

    __table_args__ = (
        UniqueConstraint('page_id', 'section_index', name='uq_page_section'),
        Index('ix_sections_search_vector', 'search_vector', postgresql_using='gin'),
    )

