from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.ask import AskRequest, AskResponse, Citation
from app.services.retrieval import RetrievalService
from app.services.llm import LLMService
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
    Retrieves relevant sections hierarchically and generates a citation-backed answer.
    """
    logger.info(f"Received question: '{request.query}' (top_k={request.top_k}, filters={request.filters})")

    # 1. Retrieve relevant sections
    retrieval_start = time.time()
    retrieval_service = RetrievalService(db)
    results = retrieval_service.search(request.query, top_k=request.top_k, filters=request.filters)
    retrieval_time = time.time() - retrieval_start
    logger.info(f"Retrieval completed in {retrieval_time:.3f}s, found {len(results)} sections")

    # 2. Generate answer with citations
    generation_start = time.time()
    llm_service = LLMService()
    llm_output = llm_service.generate_answer(request.query, results)
    generation_time = time.time() - generation_start
    logger.info(f"LLM generation completed in {generation_time:.3f}s")

    # 3. Build response
    citations = [
        Citation(**c) for c in llm_output["citations"]
    ]

    return AskResponse(
        answer=llm_output["answer"],
        citations=citations,
    )
