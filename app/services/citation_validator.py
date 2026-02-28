"""
Deterministic Citation Validator.
Post-generation verifier that cross-checks every citation in the LLM's answer
against the actual context sources provided, ensuring citation integrity.
"""
import re
from typing import List, Dict, Any, Tuple, Set
import logging

logger = logging.getLogger(__name__)

# Pattern: [Document: filename.pdf, Page 3]
CITATION_PATTERN = re.compile(
    r'\[Document:\s*([^,\]]+),\s*Page\s*(\d+)\]',
    re.IGNORECASE
)


class CitationValidator:
    """
    Validates that citations in the LLM's answer correspond to actual source context.
    """

    def validate(
        self,
        answer: str,
        context_sources: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Validate citations in the LLM answer against actual sources.

        Args:
            answer: The LLM-generated answer text.
            context_sources: List of dicts with 'document_name' and 'page_number' keys.

        Returns:
            Dict with 'verified_citations', 'unverified_citations', and 'citation_integrity'.
        """
        # Build the set of valid (document, page) pairs from actual sources
        valid_sources: Set[Tuple[str, int]] = set()
        for src in context_sources:
            valid_sources.add((
                src["document_name"].strip().lower(),
                src["page_number"],
            ))

        # Extract all citations from the answer
        found_citations = CITATION_PATTERN.findall(answer)

        if not found_citations:
            logger.info("No citations found in LLM answer")
            return {
                "verified_citations": [],
                "unverified_citations": [],
                "citation_integrity": 1.0 if not context_sources else 0.0,
            }

        verified = []
        unverified = []

        for doc_name, page_str in found_citations:
            doc_name_clean = doc_name.strip()
            page_num = int(page_str)
            citation_str = f"[Document: {doc_name_clean}, Page {page_num}]"

            if (doc_name_clean.lower(), page_num) in valid_sources:
                verified.append(citation_str)
            else:
                unverified.append(citation_str)

        total = len(verified) + len(unverified)
        integrity = len(verified) / total if total > 0 else 1.0

        logger.info(
            f"Citation validation: {len(verified)} verified, "
            f"{len(unverified)} unverified, integrity={integrity:.2f}"
        )

        return {
            "verified_citations": verified,
            "unverified_citations": unverified,
            "citation_integrity": round(integrity, 4),
        }
