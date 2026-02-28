from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from app.core.config import settings
from app.services.retrieval import RetrievalResult
import logging
import json

logger = logging.getLogger(__name__)

CITATION_SYSTEM_PROMPT = """You are a helpful research assistant. Answer the user's question using ONLY the provided context sections.

RULES:
1. Base your answer strictly on the provided context. Do not use outside knowledge.
2. For every claim or statement, include a citation in the format [Document: <filename>, Page <number>].
3. If the context does not contain enough information to answer, say "I don't have enough information to answer this question."
4. Be concise and accurate.
"""


def format_context(results: List[RetrievalResult]) -> str:
    """Format retrieval results into a labeled context block for the LLM."""
    context_parts = []
    for i, r in enumerate(results):
        label = f"[Source {i+1}: {r.document_filename}, Page {r.page_number}]"
        title = f" - Section: {r.section_title}" if r.section_title else ""
        context_parts.append(f"{label}{title}\n{r.section_content}")
    return "\n\n---\n\n".join(context_parts)


class LLMProvider(ABC):
    """Abstract base class for LLM providers."""

    @abstractmethod
    def generate(self, system_prompt: str, user_prompt: str) -> str:
        pass


class MockLLMProvider(LLMProvider):
    """Mock LLM for testing — echoes a structured response using the context."""

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        return (
            f"Based on the provided documents, here is the answer to your question.\n\n"
            f"[This is a mock response. In production, a real LLM would generate a "
            f"citation-backed answer using the context provided in the system prompt.]"
        )


class GeminiLLMProvider(LLMProvider):
    """Google Gemini LLM integration."""

    def __init__(self, api_key: str, model_name: str = "gemini-2.0-flash"):
        try:
            from google import genai
            self.client = genai.Client(api_key=api_key)
            self.model_name = model_name
            logger.info(f"Initialized GeminiLLMProvider with model: {model_name}")
        except ImportError:
            raise ImportError("google-genai package required. Install with: pip install google-genai")

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        from google.genai import types
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=user_prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                temperature=0.3,
                max_output_tokens=1024,
            ),
        )
        return response.text


class LLMService:
    """
    Orchestrates LLM-powered answer generation with citation enforcement.
    """

    def __init__(self):
        self.provider = self._create_provider()

    def _create_provider(self) -> LLMProvider:
        provider_name = settings.LLM_PROVIDER.lower()
        if provider_name == "gemini":
            return GeminiLLMProvider(api_key=settings.LLM_API_KEY)
        elif provider_name == "mock":
            logger.info("Using MockLLMProvider")
            return MockLLMProvider()
        else:
            logger.warning(f"Unknown LLM_PROVIDER '{provider_name}', falling back to mock")
            return MockLLMProvider()

    def generate_answer(self, query: str, results: List[RetrievalResult]) -> Dict[str, Any]:
        """
        Generate a citation-backed answer from retrieved context.

        Args:
            query: The user's question.
            results: List of RetrievalResult from the RetrievalService.

        Returns:
            Dict with 'answer' and 'citations' keys.
        """
        if not results:
            return {
                "answer": "I don't have enough information to answer this question. No relevant sections were found.",
                "citations": [],
            }

        context_text = format_context(results)
        user_prompt = f"Context:\n{context_text}\n\nQuestion: {query}"

        logger.info(f"Generating answer with {len(results)} context sections")

        try:
            answer = self.provider.generate(CITATION_SYSTEM_PROMPT, user_prompt)
        except Exception as e:
            logger.error(f"LLM generation failed: {str(e)}", exc_info=True)
            raise

        # Build citation list from the results used
        citations = []
        seen = set()
        for r in results:
            key = (r.document_filename, r.page_number)
            if key not in seen:
                seen.add(key)
                citations.append({
                    "document_name": r.document_filename,
                    "page_number": r.page_number,
                    "section_title": r.section_title,
                    "text_snippet": r.section_content[:150] + "..." if len(r.section_content) > 150 else r.section_content,
                })

        return {
            "answer": answer,
            "citations": citations,
        }
