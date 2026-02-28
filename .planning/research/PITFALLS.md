# Pitfalls Research

**Domain:** Hierarchical RAG / Knowledge Base
**Researched:** 2026-03-01
**Confidence:** HIGH

## Critical Pitfalls

### Pitfall 1: Dual-Write Inconsistency

**What goes wrong:**
Vector data in Qdrant and hierarchical metadata in PostgreSQL fall out of sync.

**Why it happens:**
Writing to two separate databases isn't inherently transactional. If Postgres succeeds but Qdrant fails (or vice versa), the index is corrupt.

**How to avoid:**
For v1 MVP, use robust try-catch blocks and transaction rollbacks on the relational side if the vector insert fails, or a simple transactional outbox pattern.

**Warning signs:**
Users ask questions and the system crashes trying to fetch metadata for a vector ID that doesn't exist in Postgres.

**Phase to address:**
Phase 1: Foundation (Database setup and Repository patterns)

---

### Pitfall 2: Context Window Overflow

**What goes wrong:**
Hierarchical retrieval pulls too many pages/sections, exceeding the LLM's context window.

**Why it happens:**
Greedy retrieval without reranking or token counting limits.

**How to avoid:**
Implement strict token-counting limits in the LLM Orchestrator Service. If results exceed limits, prioritize by relevance score and truncate gracefully.

**Warning signs:**
400 Bad Request errors from the OpenAI/Anthropic API due to `max_tokens` exceeded.

**Phase to address:**
Phase 3: Retrieval & LLM Generation

---

### Pitfall 3: Brittle PDF Extraction

**What goes wrong:**
PDFs with complex columns, tables, or weird encodings break the ingestion pipeline, resulting in garbage text.

**Why it happens:**
Assuming all PDFs are simple linear text.

**How to avoid:**
Use a robust library like PyMuPDF. Handle exceptions gracefully and store the raw text alongside the parsed hierarchy so debugging is possible.

**Warning signs:**
Citations point to gibberish text.

**Phase to address:**
Phase 2: Ingestion Pipeline

## Technical Debt Patterns

| Shortcut | Immediate Benefit | Long-term Cost | When Acceptable |
|----------|-------------------|----------------|-----------------|
| Skipping interfaces / Dependency Injection | Faster initial coding | Harder to test and swap implementations (e.g., swapping OpenAI for local LLMs) | Never. We committed to clean architecture. |

---
*Pitfalls research for: Hierarchical RAG / Knowledge Base*
*Researched: 2026-03-01*
