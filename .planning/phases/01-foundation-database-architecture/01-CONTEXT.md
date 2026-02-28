# Phase 01: Foundation (Database & Architecture) - Context

**Gathered:** 2026-03-01
**Status:** Ready for planning

<domain>
## Phase Boundary

Establish a production-ready, modular base with all storage connections, config management, and generalized interfaces. We'll clarify HOW to implement this without adding capabilities belonging to ingestion or retrieval.

</domain>

<decisions>
## Implementation Decisions

### Database Schema & Invariants
- Enforce hierarchy strictly at PostgreSQL level using foreign key constraints.
- Each Page must have NOT NULL document_id with ON DELETE CASCADE.
- Each Section must have NOT NULL page_id with ON DELETE CASCADE.
- Section embedding in Qdrant must reference Section primary key (UUID).
- Use UUIDs for Document, Page, Section for global uniqueness.
- Add unique constraint on (document_id, page_number).
- Add unique constraint on (page_id, section_index).
- No application-level enforcement for hierarchy integrity — DB must guarantee it.

### Observability Detail
- Structured JSON logging.
- Include request_id (generated per request).
- Log: ingestion start/end, embedding generation time, Qdrant/Postgres write success/failure, retrieval latency, LLM latency.
- Use standard logging module with JSON formatter.
- No external observability stack yet (Prometheus deferred).

### API Design
- Prefix all endpoints with `/api/v1`.
- Use dependency injection for DB session, Qdrant client, and Settings.
- Endpoints: `POST /api/v1/documents`, `POST /api/v1/ask`, `GET /api/v1/health`.
- Keep routers separated by domain (`documents.py`, `ask.py`).
- No authentication in v1 but include middleware stub for future expansion.

### Configuration & Secrets
- Use Pydantic `BaseSettings` for config management.
- Load from `.env` for local development (provide `.env.example`).
- Config fields: `POSTGRES_URL`, `QDRANT_URL`, `EMBEDDING_MODEL_NAME`, `LLM_PROVIDER`, `LLM_API_KEY`.
- No hardcoded secrets.

</decisions>

<code_context>
## Existing Code Insights

### Reusable Assets
- [None — Greenfield project]

### Established Patterns
- [None — Establishing new patterns based on standard clean architecture & FastAPI best practices]

### Integration Points
- [New API layer connecting to Postgres and Qdrant]

</code_context>

<specifics>
## Specific Ideas

- Qdrant must function strictly as a vector index; PostgreSQL must function as the canonical source of truth for all metadata.
- Embedding provider interface must be abstract (no hardcoded dims) so swapping is trivial later.

</specifics>

<deferred>
## Deferred Ideas

- Prometheus/Grafana or other external observability stacks (deferred beyond v1).
- Kafka streaming / async queue ingestion (deferred to v1.x).
- True authentication (stubs only for v1).

</deferred>

---

*Phase: 01-foundation-database-architecture*
*Context gathered: 2026-03-01*
