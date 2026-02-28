# Roadmap: PageIndex-KnowledgeOS

## Overview

A phased execution plan to build an enterprise-grade hierarchical RAG system. We will start by laying down the infrastructure and clean architecture boundaries, followed by the rigorous ingestion pipeline mapping PDFs to a Document → Page → Section hierarchy. Finally, we'll implement the hierarchical retrieval and LLM citation generation logic.

## Phases

- [ ] **Phase 1: Foundation (Database & Architecture)** - Base FastAPI, Docker, and Database patterns.
- [ ] **Phase 2: Ingestion Pipeline** - PDF parsing, embedding generation, and dual-db insertion.
- [ ] **Phase 3: Retrieval & LLM Generation** - Hierarchical search and citation-backed answer generation.

## Phase Details

### Phase 1: Foundation (Database & Architecture)
**Goal**: Establish a production-ready, modular base with all storage connections.
**Depends on**: Nothing (first phase)
**Requirements**: API-01, INF-01
**Success Criteria** (what must be TRUE):
  1. FastAPI server runs locally via Docker Compose alongside Qdrant and PostgreSQL.
  2. SQLAlchemy models and database migrations for the hierarchy are defined and applied.
  3. Qdrant collections are initialized and reachable.
**Plans**: 3 plans

Plans:
- [ ] 01-01: Define FastAPI project structure, config, and Docker Compose with DB services.
- [ ] 01-02: Implement PostgreSQL connection, SQLAlchemy models (Document, Page, Section), and Alembic migrations.
- [ ] 01-03: Implement Qdrant connection management and collection initialization scripts.

### Phase 2: Ingestion Pipeline
**Goal**: Convert raw PDFs into structured, embedded data across both databases.
**Depends on**: Phase 1
**Requirements**: INGST-01, INGST-02, IDX-01, IDX-02, IDX-03
**Success Criteria** (what must be TRUE):
  1. A multi-page PDF can be uploaded via the API.
  2. The PDF is parsed into a strict hierarchy (Document -> Pages -> Sections).
  3. Sections are embedded and successful writes occur in both PostgreSQL and Qdrant.
**Plans**: 3 plans

Plans:
- [ ] 02-01: Build the PDF Extraction Service (PyMuPDF wrapper) identifying pages and logical sections.
- [ ] 02-02: Build embedding generation service (SentenceTransformers or similar wrapper).
- [ ] 02-03: Build the API endpoint and orchestration service for dual-database writes (Postgres + Qdrant) with rollback capability.

### Phase 3: Retrieval & LLM Generation
**Goal**: Retrieve data hierarchically and generate answers with trace-back citations.
**Depends on**: Phase 2
**Requirements**: RTRV-01, QNA-01, QNA-02
**Success Criteria** (what must be TRUE):
  1. Queries accurately filter and return context based on vector similarity and metadata hierarchy.
  2. LLM returns a coherent answer using the provided context.
  3. LLM answer explicitly cites the Document ID and Page/Section numbers.
**Plans**: 3 plans

Plans:
- [ ] 03-01: Implement Hierarchical Retrieval Service (query Qdrant -> intersect with Postgres metadata).
- [ ] 03-02: Implement LLM Orchestration Service with strict citation-enforcing prompts.
- [ ] 03-03: Expose `/ask` API endpoint and write end-to-end integration tests.

## Progress

**Execution Order:**
Phases execute in numeric order: 1 → 2 → 3

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Foundation | 0/3 | Not started | - |
| 2. Ingestion Pipeline | 0/3 | Not started | - |
| 3. Retrieval & LLM Generation | 0/3 | Not started | - |
