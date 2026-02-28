# Phase 04 Research: Retrieval Intelligence Upgrade

## 1. Current Architecture Gaps

### 1.1 Vector-Only Retrieval (No Keyword Signal)
**File**: `app/services/retrieval.py` L60-82  
**Problem**: `RetrievalService.search()` performs **pure vector similarity** via Qdrant `query_points`. This misses exact-match scenarios (e.g., searching for "HIPAA" returns semantically similar but irrelevant sections while missing the exact term).  
**Solution**: Introduce **Hybrid Retrieval** combining dense vectors (Qdrant) with sparse BM25 keyword scores (PostgreSQL `tsvector` or Qdrant sparse vectors). Fuse using Reciprocal Rank Fusion (RRF).

### 1.2 No Metadata Filtering
**File**: `app/services/retrieval.py` L76-80  
**Problem**: `query_points` passes no `filter` parameter. Users cannot scope searches to a specific document, page range, or date range.  
**Solution**: Accept optional filter parameters in the `/ask` request. Translate them into Qdrant `Filter` clauses and parallel PostgreSQL `WHERE` conditions.

### 1.3 No Re-Ranking Layer
**File**: `app/services/retrieval.py` L126-130  
**Problem**: Results are returned in raw Qdrant similarity order. No cross-document relevance scoring.  
**Solution**: Add a **Cross-Encoder Re-Ranker** (e.g., `cross-encoder/ms-marco-MiniLM-L-6-v2` via `sentence-transformers`) that re-scores (query, section_content) pairs after retrieval. This dramatically improves precision.

### 1.4 Naive Context Packing
**File**: `app/services/llm.py` L20-27 (`format_context`)  
**Problem**: All `top_k` sections are blindly concatenated into the prompt. No awareness of:
- Token budget (may overflow LLM context window)
- Redundancy (overlapping sections from same page)
- Relevance threshold (low-scored sections dilute quality)
**Solution**: Implement a **Context Window Packer** that:
1. Estimates token count per section
2. Packs sections greedily until budget is reached
3. Deduplicates by (document, page) proximity
4. Drops sections below a score threshold

### 1.5 Soft Citation Enforcement
**File**: `app/services/llm.py` L10-17 (`CITATION_SYSTEM_PROMPT`)  
**Problem**: The system prompt *asks* the LLM to cite but doesn't **enforce** it. The LLM may hallucinate citations, skip them, or invent [Document, Page] pairs not in the context.  
**Solution**: 
1. Structured output (JSON mode) with a `citations[]` array that maps to source indices
2. Post-generation **citation validator** that cross-checks every `[Document: X, Page Y]` against the actual context provided
3. Strip or flag unverifiable citations before returning to the user

## 2. Proposed Architecture

```
Query → EmbedQuery
            ↓
    ┌───────┴───────┐
    │               │
  Qdrant          BM25
  (dense)       (sparse)
    │               │
    └───────┬───────┘
            ↓
    Reciprocal Rank Fusion
            ↓
    Metadata Filter (Postgres canonical)
            ↓
    Cross-Encoder Re-Rank
            ↓
    Context Window Packer
            ↓
    LLM (Structured Output)
            ↓
    Citation Validator
            ↓
    Response
```

## 3. New Dependencies
- `sentence-transformers` — for cross-encoder re-ranking
- `rank_bm25` — lightweight BM25 implementation (or Qdrant sparse vectors)
- `tiktoken` — token counting for context packing

## 4. Configuration Additions
```python
# app/core/config.py additions
RERANKER_MODEL: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"
RERANKER_ENABLED: bool = True
BM25_WEIGHT: float = 0.3      # RRF weight for BM25 signal
VECTOR_WEIGHT: float = 0.7    # RRF weight for vector signal
CONTEXT_TOKEN_BUDGET: int = 3000
MIN_RELEVANCE_THRESHOLD: float = 0.1
```
