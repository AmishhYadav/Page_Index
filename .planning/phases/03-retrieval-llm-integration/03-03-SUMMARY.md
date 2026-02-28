---
phase: "03"
plan: "03-03"
subsystem: "API"
tags: ["fastapi", "ask", "e2e"]
requirements: ["QNA-01", "QNA-02"]
---
# Phase 03 Plan 03-03: /ask API & E2E Tests Summary
## Overview
Exposed `POST /api/v1/ask` endpoint and verified the complete ingestion → retrieval → generation pipeline.
## Key Files
- `app/api/v1/ask.py`: FastAPI router with per-stage latency logging.
- `app/schemas/ask.py`: Pydantic request/response models.
- `app/main.py`: Registered ask router.
## Key Decisions
- Separate retrieval and generation latency logging for observability.
- Citations are always returned alongside the answer (even with mock LLM).
## Self-Check: PASSED
