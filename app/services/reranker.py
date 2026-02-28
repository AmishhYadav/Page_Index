"""
Cross-Encoder Re-Ranking Service.
Re-scores (query, section_content) pairs using a cross-encoder model
to dramatically improve retrieval precision before LLM generation.
"""
from typing import List, Optional
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

# Lazy-loaded singleton to avoid blocking app startup
_reranker_model = None


def _get_reranker():
    """Lazy-load the cross-encoder model."""
    global _reranker_model
    if _reranker_model is None:
        try:
            from sentence_transformers import CrossEncoder
            logger.info(f"Loading cross-encoder model: {settings.RERANKER_MODEL}")
            _reranker_model = CrossEncoder(settings.RERANKER_MODEL)
            logger.info("Cross-encoder model loaded successfully")
        except ImportError:
            logger.error("sentence-transformers not installed. Install with: pip install sentence-transformers")
            return None
        except Exception as e:
            logger.error(f"Failed to load cross-encoder model: {e}", exc_info=True)
            return None
    return _reranker_model


class ReRanker:
    """
    Re-ranks retrieval results using a cross-encoder model.
    Can be toggled on/off via RERANKER_ENABLED config.
    """

    def rerank(self, query: str, results: List, top_n: Optional[int] = None) -> List:
        """
        Re-rank retrieval results using cross-encoder scoring.

        Args:
            query: The user's search query.
            results: List of RetrievalResult objects.
            top_n: Optional limit on number of results to return.

        Returns:
            Re-ranked list of RetrievalResult objects.
        """
        if not settings.RERANKER_ENABLED:
            logger.info("Re-ranking disabled (RERANKER_ENABLED=false)")
            return results

        if not results:
            return results

        model = _get_reranker()
        if model is None:
            logger.warning("Cross-encoder model unavailable, returning results without re-ranking")
            return results

        # Build (query, content) pairs for cross-encoder scoring
        pairs = [(query, r.section_content) for r in results]

        try:
            scores = model.predict(pairs)
            logger.info(f"Cross-encoder scored {len(pairs)} pairs")

            # Attach cross-encoder scores and sort
            scored_results = list(zip(results, scores))
            scored_results.sort(key=lambda x: x[1], reverse=True)

            # Update scores in results
            reranked = []
            for result, ce_score in scored_results:
                result.score = float(ce_score)
                reranked.append(result)

            if top_n:
                reranked = reranked[:top_n]

            logger.info(f"Re-ranked {len(reranked)} results (top score: {reranked[0].score:.4f})")
            return reranked

        except Exception as e:
            logger.error(f"Cross-encoder re-ranking failed: {e}", exc_info=True)
            return results  # Graceful fallback
