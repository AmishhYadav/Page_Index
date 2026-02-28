# Roadmap: PageIndex-KnowledgeOS

## Overview

A phased execution plan to build an enterprise-grade hierarchical RAG system. We will start by laying down the infrastructure, strict hierarchical models, configurable settings, and observability logging. Next, we will build the ingestion pipeline to map PDFs to the Document → Page → Section hierarchy. Finally, we'll implement the hierarchical retrieval contract and LLM citation generation logic.

## Phases

- [ ] **Phase 1: Foundation (Database & Architecture)** - Config, Modularity, Base FastAPI, Docker, Models with constraints.
- [ ] **Phase 2: Ingestion Pipeline** - PDF parsing, embedding generation, and dual-db insertion.
- [ ] **Phase 3: Retrieval & LLM Generation** - Strict hierarchical search contract and citation-backed answer generation.

## Phase Details

### Phase 1: Foundation (Database & Architecture)
**Goal**: Establish a production-ready, modular base with all storage connections, config management, and generalized interfaces.
**Depends on**: Nothing (first phase)
**Requirements**: API-01, INF-01, INF-02, INF-03, INF-04, IDX-04
**Success Criteria** (what must be TRUE):
  1. FastAPI server runs locally via Docker Compose alongside Qdrant and PostgreSQL.
  2. Centralized settings via Pydantic using Env Vars are active.
  3. SQLAlchemy models (Document, Page, Section) enforce strict hierarchy and cascading deletes.
  4. Embedding provider interface is abstracted and dimension-agnostic.
  5. System logs ingestion/embedding errors and retrieval latency.
**Plans**: 4 plans

Plans:
- [ ] 01-01: Define FastAPI project structure, centralized Pydantic configuration, and Docker Compose with DB services.
- [ ] 01-02: Implement PostgreSQL connection, SQLAlchemy models with strict Document -> Page -> Section cascading invariants, and Alembic migrations.
- [ ] 01-03: Abstract embedding provider interface (no hardcoded dims) and implement generalized observability logging wrapper.
- [ ] 01-04: Implement Qdrant connection management and collection initialization scripts based on Pydantic config.

### Phase 2: Ingestion Pipeline
**Goal**: Convert raw PDFs into structured, embedded data across both databases uniquely tied to primary keys.
**Depends on**: Phase 1
**Requirements**: INGST-01, INGST-02, IDX-01, IDX-02, IDX-03, IDX-05
**Success Criteria** (what must be TRUE):
  1. A multi-page PDF can be uploaded via the API.
  2. The PDF is parsed into a strict hierarchy (Document -> Pages -> Sections).
  3. Sections are embedded and successful writes occur in PostgreSQL (canonical) and Qdrant (vectors only, uniquely linked to PK).
**Plans**: 3 plans

Plans:
- [ ] 02-01: Build the PDF Extraction Service (PyMuPDF wrapper) identifying pages and logical sections.
- [ ] 02-02: Build the API endpoint and orchestration service prioritizing Postgres as the canonical source.
- [ ] 02-03: Implement reliable database sync logic: write hierarchy to Postgres, embed sections, and write to Qdrant linked exactly to the Section PK.

### Phase 3: Retrieval & LLM Generation
**Goal**: Retrieve data following the strict retrieval contract and generate answers with trace-back citations.
**Depends on**: Phase 2
**Requirements**: RTRV-01, RTRV-02, RTRV-03, QNA-01, QNA-02
**Success Criteria** (what must be TRUE):
  1. Retrieval queries Qdrant for vectors, then fetches canonical hierarchy constraints strictly from Postgres.
  2. Retrieved blocks are grouped and ranked by Document/Page relevance.
  3. LLM returns a coherent answer using the provided context and includes explicit Document/Page citations.
**Plans**: 3 plans

Plans:
- [ ] 03-01: Implement Retrieval Service contract: embed query -> top-k Qdrant sections -> fetch canonical Postgres metadata -> group/rank.
- [ ] 03-02: Implement LLM Orchestration Service with strict citation-enforcing prompts.
- [ ] 03-03: Expose `/ask` API endpoint, instrument retrieval latency logging, and write E2E integration tests.

## Progress

**Execution Order:**
Phases execute in numeric order: 1 → 2 → 3

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Foundation | 0/4 | Not started | - |
| 2. Ingestion Pipeline | 0/3 | Not started | - |
| 3. Retrieval & LLM Gen | 0/3 | Not started | - |
