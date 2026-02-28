# Stack Research

**Domain:** Hierarchical RAG / Knowledge Base
**Researched:** 2026-03-01
**Confidence:** HIGH

## Recommended Stack

### Core Technologies

| Technology | Version | Purpose | Why Recommended |
|------------|---------|---------|-----------------|
| Python | 3.12+ | Core Language | Standard for AI/ML and data pipelines. Excellent async support. |
| FastAPI | 0.110+ | REST API Framework | High performance, native async, automatic OpenAPI generation. |
| Qdrant | 1.8+ | Vector Database | Highly scalable, excellent metadata filtering capabilities essential for hierarchical retrieval. |
| PostgreSQL | 16+ | Relational metadata store | ACID compliance guarantees for document hierarchies, versions, and timestamp tracking. |
| SQLAlchemy | 2.0+ | ORM | Type-safe, production-ready relational data access. |
| OpenAI API / Anthropic API | Latest | LLM Generation | Industry leaders for citation-backed text generation. |

### Supporting Libraries

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| pdfplumber or PyMuPDF | Latest | PDF Extraction | For accurate page and logical section extraction. |
| Pydantic | 2.6+ | Data Validation | Core to FastAPI, ensures robust schema definition for APIs and internal interfaces. |
| Sentence-Transformers / OpenAI | Latest | Embeddings | Generating high-quality vector embeddings for sections. |

### Development Tools

| Tool | Purpose | Notes |
|------|---------|-------|
| Docker & Docker Compose | Containerization | Ensures environment parity and easy deployment of Qdrant/PostgreSQL alongside the app. |
| pytest, pytest-asyncio | Testing | Robust test suite for both sync and async functions. |
| Ruff & mypy | Linting & Type Checking | Enforces clean architecture and typing constraints. |

## Installation

```bash
# Core
pip install fastapi uvicorn qdrant-client psycopg2-binary sqlalchemy pydantic

# AI & Processing
pip install openai pymupdf sentence-transformers

# Dev dependencies
pip install pytest pytest-asyncio ruff mypy
```

## Alternatives Considered

| Recommended | Alternative | When to Use Alternative |
|-------------|-------------|-------------------------|
| Qdrant | Milvus / Pinecone | Pinecone if fully managed SaaS is required; Milvus for extreme massive-scale self-hosted. Qdrant hits the sweet spot for Docker-ready, metadata-heavy workloads. |
| PostgreSQL | MongoDB | MongoDB is easier for unstructured data, but PostgreSQL is far superior for maintaining strict structural hierarchies (Document -> Page -> Section). |

## What NOT to Use

| Avoid | Why | Use Instead |
|-------|-----|-------------|
| LangChain | Can become bloated and abstract away the clean architecture needed for custom hierarchical retrieval. | Custom orchestration using pure Python, Pydantic, and official SDKs. |

---
*Stack research for: Hierarchical RAG / Knowledge Base*
*Researched: 2026-03-01*
