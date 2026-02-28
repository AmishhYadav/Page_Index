import uuid
from sqlalchemy import Column, Integer, String, Text, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.base import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    # Add other metadata fields here later as needed (e.g., source file name, hash)

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
    content = Column(Text, nullable=False)

    page = relationship("Page", back_populates="sections")

    __table_args__ = (
        UniqueConstraint('page_id', 'section_index', name='uq_page_section'),
    )
