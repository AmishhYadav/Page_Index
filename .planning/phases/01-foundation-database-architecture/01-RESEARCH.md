# Phase 01: Foundation (Database & Architecture) - Research

**Objective:** What do we need to know to plan and execute Phase 1 well?

## 1. Project Structure (FastAPI)
A clean, modular structure is necessary.
```
app/
├── api/          # Routers and endpoints (/api/v1 prefix)
│   ├── v1/
│   │   ├── documents.py
│   │   └── ask.py
│   └── deps.py   # Dependency injection objects (db, qdrant, settings)
├── core/         # Configuration, logging, observability
│   ├── config.py
│   └── logger.py
├── db/           # PostgreSQL and Qdrant connection management
│   ├── session.py
│   └── qdrant.py
├── models/       # SQLAlchemy models
├── schemas/      # Pydantic schemas for API inputs/outputs
├── services/     # Core business logic / abstract interfaces
│   └── embeddings.py
└── main.py       # FastAPI application factory
```

## 2. Pydantic Configuration (`pydantic-settings`)
- Use `pydantic-settings` to manage environment variables.
- Fields: `POSTGRES_URL`, `QDRANT_URL`, `EMBEDDING_MODEL_NAME`, `LLM_PROVIDER`, `LLM_API_KEY`.
- Provide a `config.py` that loads these and instantiates a centralized `Settings` object.

## 3. SQLAlchemy Models & Constraints
- **Document**: `id` (UUID, primary key), metadata.
- **Page**: `id` (UUID), `document_id` (UUID, foreign key, `ondelete="CASCADE"`), `page_number` (int). 
  - `UniqueConstraint('document_id', 'page_number', name='uq_doc_page')`
- **Section**: `id` (UUID), `page_id` (UUID, foreign key, `ondelete="CASCADE"`), `section_index` (int), `content` (text).
  - `UniqueConstraint('page_id', 'section_index', name='uq_page_section')`
- **Migrations**: Use `alembic` to auto-generate and apply schema migrations.

## 4. Qdrant Setup
- Use `qdrant-client` (`AsyncQdrantClient`).
- Qdrant collections require a fixed dimensionality on creation. However, since the embedding model is configurable and dimensionality shouldn't be hardcoded, the initialization script needs to query the active embedding model for its output dimension *before* creating the Qdrant collection, or rely on a config mapping. 
- The payload in Qdrant will only strictly need to link to the Section PK (`section_id`).

## 5. Embedding Provider Abstraction
- Create an Abstract Base Class (ABC) `EmbeddingProvider` with methods like `get_dimension()` and `embed(texts: List[str]) -> List[List[float]]`.
- This ensures that if the model is swapped via config, the system gracefully adapts.

## 6. Observability & Logging
- Use standard library `logging` and a JSON formatter like `python-json-logger`.
- Include a middleware in FastAPI that generates a `request_id` (UUID) for each request, uses `contextvars` to store it, and attaches it to all log records.
- Logging points: ingestion start/end, embedding generation, Qdrant/Postgres write status, retrieval, and LLM latencies. We can use structural logs like `{"event": "qdrant_write", "status": "success", "duration_ms": 45}`.

## 7. Docker Infrastructure
- `docker-compose.yml` to spin up:
  - `api`: FastAPI application (build from local Dockerfile)
  - `postgres`: official `postgres:15-alpine`
  - `qdrant`: official `qdrant/qdrant:latest`
- Add healthchecks for `postgres` and `qdrant` to ensure the API container waits for them to be ready.

## Validation Architecture
- **Schema Validation**: Verify Alembic migrations apply cleanly and Postgres constraints correctly reject duplicates or orphan records.
- **Config Validation**: Test loading an invalid `.env` or missing variables successfully throws Pydantic validation errors.
- **Docker Validation**: Verify `docker compose up` results in 3 healthy, connected containers.
