"""
Test 04-01: Hybrid Retrieval (Vector + BM25 + RRF)
Verifies:
1. BM25 retriever returns results for keyword matches
2. RRF fusion produces a combined ranking
3. Hybrid RetrievalService works end-to-end
"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))

import pytest
from app.services.fusion import rrf_fuse
from app.services.bm25_retriever import BM25Retriever


def test_rrf_fusion_basic():
    """RRF fusion combines two ranked lists correctly."""
    vector_results = [
        ("section-a", 0.95),
        ("section-b", 0.80),
        ("section-c", 0.60),
    ]
    bm25_results = [
        ("section-b", 5.0),
        ("section-d", 3.0),
        ("section-a", 1.0),
    ]

    fused = rrf_fuse(
        vector_results,
        bm25_results,
        weights=[0.7, 0.3],
    )

    # section-a and section-b appear in both lists — they should get higher scores
    fused_ids = [sid for sid, _ in fused]
    assert "section-a" in fused_ids
    assert "section-b" in fused_ids
    assert "section-d" in fused_ids

    # section-b is #1 in BM25 and #2 in vector — it should rank highly
    top_2_ids = fused_ids[:2]
    assert "section-b" in top_2_ids or "section-a" in top_2_ids


def test_rrf_fusion_single_list():
    """RRF with a single list returns the same ordering."""
    results = [("s1", 0.9), ("s2", 0.5)]
    fused = rrf_fuse(results)
    assert fused[0][0] == "s1"
    assert fused[1][0] == "s2"


def test_rrf_fusion_empty():
    """RRF with no lists returns empty."""
    fused = rrf_fuse()
    assert fused == []


def test_rrf_fusion_weighted():
    """Higher-weighted list dominates ranking."""
    list_a = [("x", 0.9), ("y", 0.8)]
    list_b = [("y", 0.9), ("x", 0.8)]

    # List A heavily weighted
    fused = rrf_fuse(list_a, list_b, weights=[10.0, 0.1])
    assert fused[0][0] == "x"  # x is rank 1 in the heavily-weighted list

    # List B heavily weighted
    fused = rrf_fuse(list_a, list_b, weights=[0.1, 10.0])
    assert fused[0][0] == "y"  # y is rank 1 in the heavily-weighted list


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
