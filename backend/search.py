import re
import logging

logger = logging.getLogger(__name__)


class SearchEngine:
    def __init__(self, indexer):
        self.indexer = indexer

    def search(self, query):
        """Search the index and return ranked results."""
        if not query or not query.strip():
            return []

        # Tokenize query same way as indexer
        query_terms = self.indexer._tokenize(query)

        if not query_terms:
            # If all terms were stop words, try raw terms
            raw_terms = re.findall(r'[a-z0-9]+', query.lower())
            query_terms = [t for t in raw_terms if len(t) > 1]

        if not query_terms:
            return []

        # Calculate TF-IDF scores for each document
        scores = {}
        matched_terms = {}

        for term in query_terms:
            idf = self.indexer.get_idf(term)
            postings = self.indexer.get_postings(term)

            for url, tf in postings.items():
                tf_idf = tf * idf
                scores[url] = scores.get(url, 0) + tf_idf

                if url not in matched_terms:
                    matched_terms[url] = set()
                matched_terms[url].add(term)

        if not scores:
            return []

        # Boost score for documents matching more query terms
        for url in scores:
            term_coverage = len(matched_terms.get(url, set())) / len(query_terms)
            scores[url] *= (1 + term_coverage)  # boost by coverage

        # Sort by score descending
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)

        # Build results
        results = []
        for url, score in ranked:
            doc = self.indexer.get_document(url)
            if doc:
                results.append({
                    "url": doc.get("url", url),
                    "title": doc.get("title", "Untitled"),
                    "description": doc.get("description", ""),
                    "score": round(score, 4),
                    "word_count": doc.get("word_count", 0),
                    "matched_terms": list(matched_terms.get(url, [])),
                })

        return results
