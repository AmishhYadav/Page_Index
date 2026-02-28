# Requirements: PageIndex-KnowledgeOS

**Defined:** 2026-03-01
**Core Value:** Structural, hierarchical document understanding and retrieval (Document → Page → Section) that prevents the context loss typical of flat-chunking RAG systems.

## v1 Requirements

### Ingestion

- [ ] **INGST-01**: System provides an API endpoint to upload PDF documents.
- [ ] **INGST-02**: System extracts text while preserving physical pages and logical sections.

### Indexing

- [ ] **IDX-01**: System generates vector embeddings for each logical section.
- [ ] **IDX-02**: System stores embeddings in Qdrant with attached metadata (doc_id, page_num, section_id).
- [ ] **IDX-03**: System stores hard hierarchical metadata and document state in PostgreSQL.
- [x] **IDX-04**: System enforces strict hierarchy invariants: Section belongs to exactly one Page, Page belongs to exactly one Document; cascading deletes applied.
- [ ] **IDX-05**: Section embeddings must be uniquely linked to their Section primary key.

### Retrieval & Generation

- [ ] **RTRV-01**: System performs hierarchical semantic search.
- [ ] **RTRV-02**: Retrieval strictly follows: embed query → Qdrant search → fetch canonical hierarchy from Postgres → group/rank by relevance.
- [ ] **RTRV-03**: PostgreSQL acts as the canonical source of truth for all metadata; Qdrant is used strictly as a vector index.
- [ ] **QNA-01**: System generates a natural language answer based on retrieved sections using an LLM.
- [ ] **QNA-02**: System includes explicit citations (document and page/section) in the generated answer.

### API & Infrastructure

- [x] **API-01**: System exposes REST APIs for all core actions (upload, search, ask) via FastAPI.
- [x] **INF-01**: System is fully containerized with Docker/Docker Compose.
- [x] **INF-02**: Embedding model is configurable (no hardcoded dimensionality) and supports graceful swapping of providers.
- [x] **INF-03**: System implements observability logging (ingestion errors, embedding failures, retrieval latency).
- [x] **INF-04**: System configuration is centralized using environment variables and typed with Pydantic Settings.

## Out of Scope

| Feature | Reason |
|---------|--------|
| Kafka / Async Queues | Postponed to v1.x to focus on core logic first. Background tasks will suffice for v1. |
| Redis Caching | Not required for initial functional validation. |
| User UI or Frontend | Backend OS/API only. |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| INGST-01 | Phase 2 | Pending |
| INGST-02 | Phase 2 | Pending |
| IDX-01 | Phase 2 | Pending |
| IDX-02 | Phase 2 | Pending |
| IDX-03 | Phase 2 | Pending |
| IDX-04 | Phase 1 | Complete |
| IDX-05 | Phase 2 | Pending |
| RTRV-01 | Phase 3 | Pending |
| RTRV-02 | Phase 3 | Pending |
| RTRV-03 | Phase 3 | Pending |
| QNA-01 | Phase 3 | Pending |
| QNA-02 | Phase 3 | Pending |
| API-01 | Phase 1 | Complete |
| INF-01 | Phase 1 | Complete |
| INF-02 | Phase 1 | Complete |
| INF-03 | Phase 1 | Complete |
| INF-04 | Phase 1 | Complete |

**Coverage:**
- v1 requirements: 17 total
- Mapped to phases: 17
- Unmapped: 0 ✓

---
*Requirements defined: 2026-03-01*
*Last updated: 2026-03-01 after user feedback refinements*
