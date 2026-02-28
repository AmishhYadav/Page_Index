# Project Research Summary

**Project:** PageIndex-KnowledgeOS
**Domain:** Hierarchical RAG / Knowledge Base
**Researched:** 2026-03-01
**Confidence:** HIGH

## Executive Summary

PageIndex-KnowledgeOS aims to solve the critical "context loss" problem inherent in standard flat-chunking RAG systems by preserving the structural hierarchy of ingested documents (Document → Page → Section). The standard approach for such an enterprise-grade system involves robust extraction (using tools like PyMuPDF), relational metadata tracking (PostgreSQL), and high-performance vector search (Qdrant).

The most critical risk is the dual-write inconsistency between vector stores and relational metadata stores, which will require careful transaction management or an outbox pattern. The system must also be designed with a clean, modular architecture (FastAPI for the API layer, strict Service/Domain layers) to allow for future scale using Kafka and Redis.

## Key Findings

### Recommended Stack

**Core technologies:**
- **FastAPI**: REST API Framework — Native async support, high performance.
- **Qdrant**: Vector Database — Excellent metadata filtering capabilities needed for hierarchical retrieval.
- **PostgreSQL**: Relational metadata store — ACID compliance guarantees for document hierarchies.
- **PyMuPDF**: PDF Extraction — Robust text and layout extraction for page/section detection.

### Expected Features

**Must have (table stakes):**
- PDF Ingestion and text extraction
- Vector Search and LLM Generation
- REST APIs

**Should have (competitive):**
- Hierarchical PageIndex mapping
- Citation-backed Answers with robust source traceability
- Clean modular interfaces separating ingestion from retrieval

**Defer (v2+):**
- Kafka queuing for asynchronous ingestion
- Redis caching for frequent queries

### Architecture Approach

**Major components:**
1. **API Routers (FastAPI)** — Handles HTTP requests and schema validation (Pydantic).
2. **Service Layer** — Orchestrates PDF Parsing, Embeddings, and LLM formatting.
3. **Data Access Layer** — Wraps Qdrant and PostgreSQL interactions.

### Critical Pitfalls

1. **Dual-Write Inconsistency** — Postgres metadata out of sync with Qdrant vectors; avoid via transaction guarantees.
2. **Context Window Overflow** — Greedy hierarchical retrieval exceeding max tokens; avoid via strict token-counting limits.
3. **Brittle PDF Extraction** — Failing on complex layouts; avoid via robust parsing tools (PyMuPDF) and error handling.

## Implications for Roadmap

Based on research, suggested phase structure:

### Phase 1: Foundation (Database & Architecture)
**Rationale:** Sets up the clean architecture required for the rest of the project.
**Delivers:** Docker-compose setup, FastAPI barebones, SQLAlchemy + Qdrant connections.
**Avoids:** Dual-write inconsistency by establishing repository patterns early.

### Phase 2: Ingestion Pipeline
**Rationale:** You can't retrieve what you haven't stored.
**Delivers:** PDF upload API, Page/Section extraction, Embeddings generation, DB insertion.
**Implements:** PDF Parser & Embeddings components.

### Phase 3: Retrieval & LLM Generation
**Rationale:** The core value prop, built on top of the ingested data.
**Delivers:** Hierarchical search logic (Doc->Page->Section), LLM prompt orchestration, citation formatting.
**Addresses:** Context Window Overflow by implementing token limits.

### Phase Ordering Rationale

- We must establish the data models and database connections before building the ingestion logic.
- Ingestion must happen before retrieval can be tested.
- This grouping enforces the clean architecture boundaries.

### Research Flags

- **Phase 2 (Ingestion):** May need deeper research on optimal logical section detection heuristics for different PDF layouts.

## Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| Stack | HIGH | Established industry patterns for RAG. |
| Features | HIGH | Clear requirements provided. |
| Architecture | HIGH | Standard clean architecture maps well to these requirements. |
| Pitfalls | HIGH | Known failure modes of RAG systems. |

**Overall confidence:** HIGH

---
*Research completed: 2026-03-01*
*Ready for roadmap: yes*
