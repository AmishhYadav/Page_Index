from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.ask import AskRequest, AskResponse, Citation
from app.services.retrieval import RetrievalService
from app.services.reranker import ReRanker
from app.services.llm import LLMService
from app.services.citation_validator import CitationValidator
import logging
import time

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/", response_model=AskResponse)
async def ask_question(
    request: AskRequest,
    db: Session = Depends(get_db),
):
    """
    Ask a question against the indexed document corpus.
    Pipeline: Hybrid Retrieval → Re-Ranking → Context Packing → LLM Generation → Citation Validation → Response
    """
    logger.info(f"Received question: '{request.query}' (top_k={request.top_k}, filters={request.filters})")

    # 1. Retrieve relevant sections (hybrid: vector + BM25 + RRF)
    retrieval_start = time.time()
    retrieval_service = RetrievalService(db)
    results = retrieval_service.search(request.query, top_k=request.top_k, filters=request.filters)
    retrieval_time = time.time() - retrieval_start
    logger.info(f"Retrieval completed in {retrieval_time:.3f}s, found {len(results)} sections")

    # 2. Re-rank results with cross-encoder (if enabled)
    rerank_start = time.time()
    reranker = ReRanker()
    results = reranker.rerank(request.query, results, top_n=request.top_k)
    rerank_time = time.time() - rerank_start
    logger.info(f"Re-ranking completed in {rerank_time:.3f}s")

    # 3. Generate answer with citations (includes context packing)
    generation_start = time.time()
    llm_service = LLMService()
    llm_output = llm_service.generate_answer(request.query, results)
    generation_time = time.time() - generation_start
    logger.info(f"LLM generation completed in {generation_time:.3f}s")

    # 4. Build citation list
    citations = [
        Citation(**c) for c in llm_output["citations"]
    ]

    # 5. Validate citations in the answer
    validator = CitationValidator()
    validation = validator.validate(
        answer=llm_output["answer"],
        context_sources=[c.dict() for c in citations] if citations else [],
    )

    return AskResponse(
        answer=llm_output["answer"],
        citations=citations,
        citation_integrity=validation["citation_integrity"],
        unverified_citations=validation["unverified_citations"],
    )

