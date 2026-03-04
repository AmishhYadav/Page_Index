import math
import re
from collections import defaultdict, Counter
import logging
import json
import os

logger = logging.getLogger(__name__)

# Common English stop words
STOP_WORDS = {
    "a", "an", "the", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "by", "from", "is", "are", "was", "were", "be", "been",
    "being", "have", "has", "had", "do", "does", "did", "will", "would",
    "could", "should", "may", "might", "shall", "can", "need", "dare",
    "it", "its", "this", "that", "these", "those", "i", "me", "my",
    "we", "our", "you", "your", "he", "him", "his", "she", "her",
    "they", "them", "their", "what", "which", "who", "whom", "where",
    "when", "why", "how", "not", "no", "nor", "as", "if", "then",
    "than", "too", "very", "just", "about", "above", "after", "again",
    "all", "also", "am", "any", "because", "before", "between", "both",
    "each", "few", "more", "most", "other", "out", "over", "own",
    "same", "so", "some", "such", "up", "down", "only", "into",
}

DATA_FILE = os.path.join(os.path.dirname(__file__), "index_data.json")


class Indexer:
    def __init__(self):
        self.documents = {}         # url -> {title, description, content, ...}
        self.inverted_index = defaultdict(dict)  # term -> {url: tf}
        self.doc_lengths = {}       # url -> number of terms
        self._load()

    def _tokenize(self, text):
        """Tokenize and normalize text."""
        if not text:
            return []
        text = text.lower()
        tokens = re.findall(r'[a-z0-9]+', text)
        tokens = [t for t in tokens if t not in STOP_WORDS and len(t) > 1]
        return tokens

    def add_document(self, page_data):
        """Add a document to the index."""
        url = page_data.get("url", "")
        if not url:
            return

        title = page_data.get("title", "")
        description = page_data.get("description", "")
        content = page_data.get("content", "")
        headings = page_data.get("headings", [])

        # Combine text with title/headings weighted more
        full_text = f"{title} {title} {title} {' '.join(headings)} {' '.join(headings)} {description} {content}"
        tokens = self._tokenize(full_text)

        if not tokens:
            logger.warning(f"No tokens extracted from {url}")
            # Still store the document metadata
            self.documents[url] = {
                "url": url,
                "title": title or "Untitled",
                "description": description,
                "word_count": 0,
            }
            self.doc_lengths[url] = 0
            self._save()
            return

        # Calculate term frequencies
        term_counts = Counter(tokens)
        doc_length = len(tokens)
        self.doc_lengths[url] = doc_length

        # Remove old index entries if re-indexing
        self._remove_from_index(url)

        # Add to inverted index with normalized TF
        for term, count in term_counts.items():
            self.inverted_index[term][url] = count / doc_length  # normalized TF

        # Store document metadata
        self.documents[url] = {
            "url": url,
            "title": title or "Untitled",
            "description": description,
            "word_count": len(page_data.get("content", "").split()),
        }

        self._save()
        logger.info(f"Indexed {url}: {len(term_counts)} unique terms, {doc_length} total tokens")

    def _remove_from_index(self, url):
        """Remove a URL from the inverted index."""
        terms_to_remove = []
        for term, postings in self.inverted_index.items():
            if url in postings:
                del postings[url]
                if not postings:
                    terms_to_remove.append(term)
        for term in terms_to_remove:
            del self.inverted_index[term]

    def remove_document(self, url):
        """Remove a document completely."""
        if url not in self.documents:
            return False
        self._remove_from_index(url)
        del self.documents[url]
        self.doc_lengths.pop(url, None)
        self._save()
        return True

    def is_indexed(self, url):
        """Check if a URL is already indexed."""
        return url in self.documents

    def get_document_count(self):
        return len(self.documents)

    def get_term_count(self):
        return len(self.inverted_index)

    def get_all_documents(self):
        return list(self.documents.values())

    def get_idf(self, term):
        """Calculate IDF for a term."""
        n = len(self.documents)
        if n == 0:
            return 0
        df = len(self.inverted_index.get(term, {}))
        if df == 0:
            return 0
        return math.log((n + 1) / (df + 1)) + 1  # smoothed IDF

    def get_postings(self, term):
        """Get postings list for a term."""
        return self.inverted_index.get(term, {})

    def get_document(self, url):
        """Get document metadata."""
        return self.documents.get(url)

    def _save(self):
        """Persist index to disk."""
        try:
            data = {
                "documents": self.documents,
                "inverted_index": dict(self.inverted_index),
                "doc_lengths": self.doc_lengths,
            }
            with open(DATA_FILE, "w") as f:
                json.dump(data, f)
        except Exception as e:
            logger.error(f"Failed to save index: {e}")

    def _load(self):
        """Load index from disk."""
        try:
            if os.path.exists(DATA_FILE):
                with open(DATA_FILE, "r") as f:
                    data = json.load(f)
                self.documents = data.get("documents", {})
                self.inverted_index = defaultdict(dict, {
                    k: v for k, v in data.get("inverted_index", {}).items()
                })
                self.doc_lengths = data.get("doc_lengths", {})
                logger.info(f"Loaded index: {len(self.documents)} documents, {len(self.inverted_index)} terms")
        except Exception as e:
            logger.error(f"Failed to load index: {e}")
            self.documents = {}
            self.inverted_index = defaultdict(dict)
            self.doc_lengths = {}
