# Phase 03 Research: Retrieval & LLM Integration

## 1. Retrieval Strategy: Hierarchical Semantic Search

The core objective is to move beyond flat chunking by leveraging our Document -> Page -> Section hierarchy.

### 1.1 The Retrieval Contract (RTRV-02)
Standard RAG retrieves N most similar chunks. Our system must:
1. **Vector Search**: Query Qdrant for the top-K `Section` embeddings.
2. **Canonical Fetch**: Use the Section IDs (UUIDs) returned by Qdrant to fetch the full hierarchical metadata from PostgreSQL.
3. **Hierarchy Context**: Retrieve parent `Page` and `Document` info for each section to provide context and citation data.
4. **Re-ranking/Grouping**: Group sections by `document_id`. If multiple sections from the same page are retrieved, they should be merged or ranked to provide a cohesive context.

### 1.2 Qdrant Retrieval
Points in Qdrant store:
- `id`: Section UUID
- `payload`: `{ "document_id": "...", "page_number": ..., "section_title": "..." }`

We will use the Qdrant client to perform a similarity search.

## 2. LLM Integration & Citations (QNA-01, QNA-02)

### 2.1 LLM Choice
We will use an OpenAI-compatible interface (likely Gemini via standard libraries) for text generation.

### 2.2 Prompt Engineering for Citations
The prompt must strictly enforce the following format:
> "According to [Document Name, Page X], the system architecture is..."

We will define a system prompt that:
- Injects the retrieved Sections as context.
- Explicitly lists available documents and their page numbers.
- Requires the LLM to include at least one citation for every major claim.

### 2.3 Data Flow
1. User Query -> `EmbeddingProvider` -> Vector Query.
2. Vector IDs -> PostgreSQL query -> Structured Context (List of Sections with Page/Doc info).
3. Structured Context + Query -> `LLMService` -> Answer with Citations.

## 3. API Implementation (`/ask`)

Endpoint: `POST /api/v1/ask`
Request Schema:
```json
{
  "query": "string",
  "top_k": 5
}
```
Response Schema:
```json
{
  "answer": "string",
  "citations": [
    {
      "document_name": "string",
      "page_number": 0,
      "text_snippet": "string"
    }
  ]
}
```

## 4. Proposed Components
- `app/services/retrieval.py`: Orchestrates Qdrant + Postgres.
- `app/services/llm.py`: Handles LLM communication and prompting.
- `app/api/v1/ask.py`: The API router.
- `app/schemas/ask.py`: Pydantic models for request/response.
