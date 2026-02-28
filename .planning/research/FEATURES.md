# Feature Research

**Domain:** Hierarchical RAG / Knowledge Base
**Researched:** 2026-03-01
**Confidence:** HIGH

## Feature Landscape

### Table Stakes (Users Expect These)

Features users assume exist. Missing these = product feels incomplete.

| Feature | Why Expected | Complexity | Notes |
|---------|--------------|------------|-------|
| PDF Ingestion | Standard format for enterprise documents | MEDIUM | Needs robust text extraction handling layouts. |
| Vector Search | Core RAG functionality | LOW | Qdrant handles this natively. |
| Generative Q&A | The point of the system | LOW | LLM integration for answering natural language questions. |

### Differentiators (Competitive Advantage)

Features that set the product apart. Not required, but valuable.

| Feature | Value Proposition | Complexity | Notes |
|---------|-------------------|------------|-------|
| Hierarchical PageIndex | Prevents context loss of flat chunking. Maps Document -> Page -> Section. | HIGH | Requires careful parsing and multi-step retrieval logic. |
| Citation-backed Answers | Builds trust, allowing users to trace claims back to original documents and pages. | MEDIUM | Needs prompt engineering to force citations based on retrieved metadata. |
| Clean Modular Interface | Separate ingestion, indexing, retrieval, and API boundaries. | MEDIUM | Future-proofs the system for Kafka/Redis integration. |

### Anti-Features (Commonly Requested, Often Problematic)

Features that seem good but create problems.

| Feature | Why Requested | Why Problematic | Alternative |
|---------|---------------|-----------------|-------------|
| Flat Chunking | "Industry standard", easy to implement. | Destroys document context; answers become unreliable out of context. | Strict hierarchical indexing. |

## Feature Dependencies

```
[PDF Ingestion]
    └──requires──> [Hierarchical Parsing]
                       └──requires──> [Embedding Generation]
                                          └──requires──> [Qdrant + Postgres Storage]

[Hierarchical Retrieval] ──requires──> [Qdrant + Postgres Storage]
    └──requires──> [LLM Generation with Citations]
```

## MVP Definition

### Launch With (v1)
- [x] PDF Ingestion API — Essential for getting data in.
- [x] Hierarchical Parsing (Doc -> Page -> Section) — Core value prop.
- [x] PostgreSQL Metadata & Qdrant Vector Storage — Foundation.
- [x] Hierarchical Retrieval Pipeline — Core value prop.
- [x] LLM Citation Generation — The user-facing feature.
- [x] Docker-ready Setup — Deployment constraint.

### Add After Validation (v1.x)
- [ ] Kafka queuing for async heavy ingestion.
- [ ] Redis caching for frequent queries.

---
*Feature research for: Hierarchical RAG / Knowledge Base*
*Researched: 2026-03-01*
