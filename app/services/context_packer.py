"""
Context Window Packing Optimizer.
Packs retrieval results into the LLM context budget by:
1. Estimating token count per section
2. Dropping sections below a relevance threshold
3. Deduplicating adjacent sections from the same (document, page)
4. Greedily packing until the token budget is exhausted
"""
from typing import List, Dict, Any, Tuple
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)


def _estimate_tokens(text: str) -> int:
    """
    Estimate token count using a simple heuristic (words * 1.3).
    This avoids importing tiktoken for lightweight operation.
    For production, swap with tiktoken.encode().
    """
    return int(len(text.split()) * 1.3)


class ContextPacker:
    """
    Packs retrieval results into a token-budget-constrained context window.
    """

    def __init__(
        self,
        token_budget: int = None,
        min_relevance: float = None,
    ):
        self.token_budget = token_budget or settings.CONTEXT_TOKEN_BUDGET
        self.min_relevance = min_relevance or settings.MIN_RELEVANCE_THRESHOLD

    def pack(self, results: List) -> Tuple[List, Dict[str, Any]]:
        """
        Pack results into the token budget.

        Args:
            results: List of RetrievalResult objects (assumed sorted by relevance).

        Returns:
            Tuple of (packed_results, metadata_dict).
        """
        if not results:
            return [], {"packed": 0, "dropped_threshold": 0, "dropped_budget": 0, "dropped_dedup": 0}

        if self.token_budget <= 0:
            # Budget of 0 means unlimited
            return results, {"packed": len(results), "dropped_threshold": 0, "dropped_budget": 0, "dropped_dedup": 0}

        dropped_threshold = 0
        dropped_dedup = 0
        dropped_budget = 0

        # Step 1: Drop below relevance threshold
        above_threshold = []
        for r in results:
            if r.score >= self.min_relevance:
                above_threshold.append(r)
            else:
                dropped_threshold += 1

        # Step 2: Deduplicate by (document, page) — keep highest-scoring per page
        seen_pages = set()
        deduped = []
        for r in above_threshold:
            page_key = (r.document_id, r.page_number)
            if page_key not in seen_pages:
                seen_pages.add(page_key)
                deduped.append(r)
            else:
                dropped_dedup += 1

        # Step 3: Greedy packing within token budget
        packed = []
        total_tokens = 0
        for r in deduped:
            section_tokens = _estimate_tokens(r.section_content)
            if total_tokens + section_tokens <= self.token_budget:
                packed.append(r)
                total_tokens += section_tokens
            else:
                dropped_budget += 1

        metadata = {
            "packed": len(packed),
            "total_tokens": total_tokens,
            "dropped_threshold": dropped_threshold,
            "dropped_dedup": dropped_dedup,
            "dropped_budget": dropped_budget,
        }

        logger.info(
            f"ContextPacker: packed {len(packed)} sections ({total_tokens} tokens), "
            f"dropped {dropped_threshold} (threshold), {dropped_dedup} (dedup), {dropped_budget} (budget)"
        )

        return packed, metadata
