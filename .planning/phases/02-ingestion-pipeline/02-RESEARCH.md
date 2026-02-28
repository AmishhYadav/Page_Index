# Phase 02: Ingestion Pipeline - Research

## Objective
Research the technical implementation of a hierarchical ingestion pipeline that converts multi-page PDFs into a structured schema (Document -> Page -> Section) with corresponding vector embeddings.

## Technical Components

### 1. PDF Extraction (PyMuPDF / fitz)
- **Capability**: PyMuPDF is selected for its high performance and ability to extract text with coordinates and font information.
- **Section Detection**: 
    - Use font size and weight to identify potential "Section Titles".
    - Fallback: Split by paragraph or predefined block size if headers are not detectable.
    - Constraint: Each Section MUST belong to a Page.
- **Page Logic**: Document structure is naturally page-oriented in PyMuPDF.

### 2. Hierarchical Mapping
- **PostgreSQL (Canonical)**:
    - Create `Document` record first.
    - Iterate `Page`s and create records.
    - Iterate `Section`s and create records.
- **Qdrant (Vectors)**:
    - Sections are the unit of embedding.
    - Each Qdrant point `id` should be the Section's UUID.
    - Metadata in Qdrant should be minimal (mostly for debugging), as PostgreSQL is the source of truth.

### 3. Orchestration Flow
1. **API Upload**: Receive file (FastAPI `UploadFile`).
2. **Parsing**: Synchronously or via background tasks (v1: background tasks via `BackgroundTasks` in FastAPI).
3. **Transactionality**:
    - Step A: Write hierarchy to Postgres (Atomic).
    - Step B: Embed all sections in batch.
    - Step C: Upsert to Qdrant.
- **Error Handling**: If Qdrant fails, log the error (Observability requirement) but Postgres remains the truth. v1 will not implement complex rollback but will log failures.

### 4. Constraints Alignment
- **Hierarchy Invariants**: Enforced by Postgres schema (cascading deletes, foreign keys).
- **Global Uniqueness**: Ensured by UUIDs generated at application level and verified by DB PKs.

## Validation Architecture
- **Unit Tests**: Mock PyMuPDF extraction to verify the section grouping logic.
- **Integration Tests**: Upload a sample 2-page PDF and verify row counts (1 Doc, 2 Pages, N Sections) and Qdrant point counts.
- **Latency Tracking**: Use the Phase 1 observability middleware to measure extraction vs embedding time.

## RESEARCH COMPLETE
