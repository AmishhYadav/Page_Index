# Architecture Research

**Domain:** Hierarchical RAG / Knowledge Base
**Researched:** 2026-03-01
**Confidence:** HIGH

## Standard Architecture

### System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                      API Layer (FastAPI)                     │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐        │
│  │ Ingest  │  │ Search  │  │  Chat   │  │ Config  │        │
│  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘        │
├───────┴────────────┴────────────┴────────────┴──────────────┤
│                   Service / Domain Layer                     │
├─────────────────────────────────────────────────────────────┤
│  ┌────────────┐  ┌─────────────┐  ┌───────────────────┐     │
│  │ PDF Parser │  │ Embeddings  │  │ LLM Orchestrator  │     │
│  └────────────┘  └─────────────┘  └───────────────────┘     │
├─────────────────────────────────────────────────────────────┤
│                    Data Access / Storage                     │
│  ┌────────────────┐  ┌──────────────────┐                   │
│  │ Qdrant (Vecs)  │  │ PostgreSQL (Meta)│                   │
│  └────────────────┘  └──────────────────┘                   │
└─────────────────────────────────────────────────────────────┘
```

### Component Responsibilities

| Component | Responsibility | Typical Implementation |
|-----------|----------------|------------------------|
| API Routers | HTTP requests, input validation | FastAPI Routers & Pydantic |
| PDF Parser | Extracting text, identifying sections/pages | PyMuPDF/pdfplumber wrapper in Services |
| Embedder | Converting section text to vectors | Sentence-transformers or OpenAI API |
| LLM Orchestrator | Formatting retrieval results into prompts, enforcing citations | Prompt templates + OpenAI API |
| Repositories | Decoupling DB logic from business logic | SQLAlchemy Repos & Qdrant Client wrappers |

## Recommended Project Structure

```
src/
├── api/                # FastAPI routers and endpoints
├── core/               # Config, logging, exceptions
├── domain/             # Pydantic models (Entities, Schemas)
├── services/           # Business logic (Ingestion, Retrieval, LLM)
├── infrastructure/     # DB connections, Qdrant client, external APIs
└── db/                 # SQLAlchemy models and migrations
```

## Data Flow

### Request Flow: Ingestion
```
[User Upload] → [API: /ingest] → [Service: Extraction] → [Service: Embed]
                                                                ↓
                                        [Storage: Postgres + Qdrant]
```

### Request Flow: Retrieval & Q&A
```
[User Query] → [API: /ask] → [Service: Embed Query]
                                     ↓
                            [Storage: Qdrant Search] → (vector matches)
                                     ↓
                 [Storage: Postgres Hierarchical Filter] → (doc -> page -> chunk)
                                     ↓
                            [Service: LLM Generation] → (answers + citations)
                                     ↓
                                [Response]
```

## Scaling Considerations

| Scale | Architecture Adjustments |
|-------|--------------------------|
| 0-1k docs | Synchronous or standard background tasks for ingestion. |
| 1k-100k docs | Message Queues (Kafka) for decoupling ingestion from API response. |
| 100k+ docs | Distributed vector DB, caching common queries (Redis). |

## Anti-Patterns

### Anti-Pattern 1: Leaking Prompts or DB connections into API Routes
**What people do:** Writing SQL or LLM calls directly in FastAPI endpoints.
**Why it's wrong:** Violates clean architecture, makes unit testing impossible.
**Do this instead:** Use the Service Layer to orchestrate domain logic.

---
*Architecture research for: Hierarchical RAG / Knowledge Base*
*Researched: 2026-03-01*
