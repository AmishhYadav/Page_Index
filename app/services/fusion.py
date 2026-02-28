"""
Reciprocal Rank Fusion (RRF) for combining ranked lists from different retrieval signals.
Paper: https://plg.uwaterloo.ca/~grbur/cormack_sigir09-rrf.pdf
"""
from typing import List, Tuple, Dict
import logging

logger = logging.getLogger(__name__)


def rrf_fuse(
    *ranked_lists: List[Tuple[str, float]],
    k: int = 60,
    weights: List[float] = None,
) -> List[Tuple[str, float]]:
    """
    Reciprocal Rank Fusion across multiple ranked result lists.

    Args:
        *ranked_lists: Variable number of ranked lists, each containing
                       (section_id, score) tuples ordered by relevance.
        k: RRF constant (default 60 per original paper).
        weights: Optional per-list weights. If None, equal weights applied.

    Returns:
        Fused list of (section_id, rrf_score) tuples, sorted descending.
    """
    if not ranked_lists:
        return []

    if weights is None:
        weights = [1.0] * len(ranked_lists)

    if len(weights) != len(ranked_lists):
        raise ValueError(f"Expected {len(ranked_lists)} weights, got {len(weights)}")

    fused_scores: Dict[str, float] = {}

    for list_idx, ranked_list in enumerate(ranked_lists):
        weight = weights[list_idx]
        for rank, (section_id, _original_score) in enumerate(ranked_list):
            rrf_score = weight * (1.0 / (k + rank + 1))
            fused_scores[section_id] = fused_scores.get(section_id, 0.0) + rrf_score

    # Sort by fused score descending
    sorted_results = sorted(fused_scores.items(), key=lambda x: x[1], reverse=True)
    logger.info(f"RRF fused {len(ranked_lists)} lists into {len(sorted_results)} unique results")
    return sorted_results
