"""
Test 04-04 & 04-05: Context Packing + Citation Validation
Verifies:
1. Context packer respects token budget and drops low-relevance items
2. Context packer deduplicates same-page sections
3. Citation validator identifies valid and invalid citations
4. Citation integrity score is calculated correctly
"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))

import pytest
from app.services.context_packer import ContextPacker, _estimate_tokens
from app.services.citation_validator import CitationValidator


# === Mock RetrievalResult for testing ===
class MockResult:
    def __init__(self, section_id, content, score, doc_id="doc1", page=1, filename="test.pdf", title="Section"):
        self.section_id = section_id
        self.section_content = content
        self.score = score
        self.document_id = doc_id
        self.page_number = page
        self.document_filename = filename
        self.section_title = title
        self.section_index = 0


# === Context Packer Tests ===

def test_packer_respects_budget():
    """Packer stops adding sections when budget is exhausted."""
    results = [
        MockResult("s1", "word " * 100, 0.9),  # ~130 tokens
        MockResult("s2", "word " * 100, 0.8, page=2),  # ~130 tokens
        MockResult("s3", "word " * 100, 0.7, page=3),  # ~130 tokens
    ]
    packer = ContextPacker(token_budget=250, min_relevance=0.0)
    packed, meta = packer.pack(results)

    # Only 2 of 3 should fit in 250 tokens (~130 each)
    assert len(packed) <= 2
    assert meta["dropped_budget"] >= 1
    assert meta["total_tokens"] <= 250


def test_packer_drops_below_threshold():
    """Packer drops sections below the relevance threshold."""
    results = [
        MockResult("s1", "high relevance content", 0.9),
        MockResult("s2", "low relevance content", 0.05, page=2),
    ]
    packer = ContextPacker(token_budget=10000, min_relevance=0.1)
    packed, meta = packer.pack(results)

    assert len(packed) == 1
    assert meta["dropped_threshold"] == 1
    assert packed[0].section_id == "s1"


def test_packer_deduplicates_same_page():
    """Packer keeps only the first (highest-scored) section per page."""
    results = [
        MockResult("s1", "first section", 0.9, page=1),
        MockResult("s2", "second section same page", 0.8, page=1),
        MockResult("s3", "different page", 0.7, page=2),
    ]
    packer = ContextPacker(token_budget=10000, min_relevance=0.0)
    packed, meta = packer.pack(results)

    assert len(packed) == 2
    assert meta["dropped_dedup"] == 1
    page_numbers = [r.page_number for r in packed]
    assert 1 in page_numbers
    assert 2 in page_numbers


def test_packer_unlimited_budget():
    """Budget of 0 returns all results."""
    results = [
        MockResult("s1", "word " * 500, 0.9),
        MockResult("s2", "word " * 500, 0.8, page=2),
    ]
    packer = ContextPacker(token_budget=0, min_relevance=0.0)
    packed, meta = packer.pack(results)

    assert len(packed) == 2
    assert meta["packed"] == 2


# === Citation Validator Tests ===

def test_validator_all_valid():
    """All citations match actual sources."""
    answer = "The system uses RAG [Document: report.pdf, Page 3] for retrieval [Document: report.pdf, Page 5]."
    sources = [
        {"document_name": "report.pdf", "page_number": 3},
        {"document_name": "report.pdf", "page_number": 5},
    ]
    validator = CitationValidator()
    result = validator.validate(answer, sources)

    assert result["citation_integrity"] == 1.0
    assert len(result["verified_citations"]) == 2
    assert len(result["unverified_citations"]) == 0


def test_validator_mixed():
    """Some citations are valid, some are fabricated."""
    answer = "Point A [Document: real.pdf, Page 1]. Point B [Document: fake.pdf, Page 99]."
    sources = [
        {"document_name": "real.pdf", "page_number": 1},
    ]
    validator = CitationValidator()
    result = validator.validate(answer, sources)

    assert result["citation_integrity"] == 0.5
    assert len(result["verified_citations"]) == 1
    assert len(result["unverified_citations"]) == 1
    assert "fake.pdf" in result["unverified_citations"][0]


def test_validator_no_citations():
    """Answer has no citations."""
    answer = "This is an answer without any citations."
    sources = [{"document_name": "test.pdf", "page_number": 1}]
    validator = CitationValidator()
    result = validator.validate(answer, sources)

    assert result["citation_integrity"] == 0.0
    assert len(result["verified_citations"]) == 0


def test_validator_empty_sources():
    """No sources and no citations → integrity 1.0."""
    answer = "No context was provided."
    sources = []
    validator = CitationValidator()
    result = validator.validate(answer, sources)

    assert result["citation_integrity"] == 1.0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
