# PageIndex-KnowledgeOS

## What This Is

An enterprise-grade hierarchical RAG system that indexes documents structurally instead of using flat chunking. It ingests PDF documents, extracts pages and logical sections, and builds a hierarchical index (Document → Page → Section) to generate citation-backed answers using an LLM.

## Core Value

Structural, hierarchical document understanding and retrieval (Document → Page → Section) that prevents the context loss typical of flat-chunking RAG systems.

## Requirements

### Validated

<!-- Shipped and confirmed valuable. -->

(None yet — ship to validate)

### Active

<!-- Current scope. Building toward these. -->

- [ ] Ingest PDF documents
- [ ] Extract pages and detect logical sections
- [ ] Build hierarchical PageIndex (Document → Page → Section)
- [ ] Store section embeddings in Qdrant
- [ ] Store metadata (document_id, page_number, section_title, version, timestamp) in PostgreSQL
- [ ] Implement hierarchical retrieval (relevant documents -> pages -> sections)
- [ ] Generate citation-backed answers using an LLM
- [ ] Expose REST APIs using FastAPI
- [ ] Ensure modular, production-structured, and Docker-ready deployment

### Out of Scope

<!-- Explicit boundaries. Includes reasoning to prevent re-adding. -->

- [Demo shortcuts] — System must be production-ready and enterprise-grade from day 1, no hacky workarounds.
- [Immediate Kafka/Redis implementation] — The architecture must be designed to scale with these later, but they are not required for the v1 implementation to keep initial scope focused.

## Context

- The system aims to solve the limitations of traditional flat-chunking RAG frameworks by preserving document hierarchy.
- Must be designed with a clean architecture separating ingestion, indexing, retrieval, LLM, and API modules.

## Constraints

- **Architecture**: Clean, Modular — Must separate ingestion, indexing, retrieval, LLM, and API modules.
- **Scalability**: Future-proof — Must be designed to scale later with Kafka and Redis.
- **Deployment**: Docker-ready — Must be containerized for consistent environments.

## Key Decisions

<!-- Decisions that constrain future work. Add throughout project lifecycle. -->

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Use Qdrant | Optimized for vector similarity search and metadata filtering | — Pending |
| Use PostgreSQL | Robust relational storage for exact metadata/hierarchy tracking | — Pending |
| Use FastAPI | High performance, async-ready REST framework | — Pending |

---
*Last updated: 2026-03-01 after initialization*
