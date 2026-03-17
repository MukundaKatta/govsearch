"""Document summarizer with extractive and LLM-based summarization."""

from __future__ import annotations

import re
from collections import Counter

from govsearch.models import GovernmentDocument


class DocumentSummarizer:
    """Summarizes government documents using extractive techniques.

    Provides extractive summarization by scoring sentences based on
    term frequency and position. Can optionally delegate to an LLM
    for abstractive summaries when an API key is configured.
    """

    def __init__(self, llm_api_key: str | None = None) -> None:
        self._llm_api_key = llm_api_key

    def summarize(
        self,
        doc: GovernmentDocument,
        max_sentences: int = 5,
        use_llm: bool = False,
    ) -> str:
        """Generate a summary of a government document.

        Args:
            doc: The document to summarize.
            max_sentences: Maximum sentences in extractive summary.
            use_llm: If True and API key is set, use LLM for abstractive summary.

        Returns:
            A summary string.
        """
        if use_llm and self._llm_api_key:
            return self._llm_summarize(doc)
        return self._extractive_summarize(doc, max_sentences)

    def summarize_section(self, text: str, max_sentences: int = 3) -> str:
        """Summarize a single section of text."""
        sentences = self._split_sentences(text)
        if len(sentences) <= max_sentences:
            return text.strip()
        scored = self._score_sentences(sentences)
        top = sorted(scored[:max_sentences], key=lambda x: x[1])
        return " ".join(s for s, _ in top)

    def key_points(self, doc: GovernmentDocument, max_points: int = 5) -> list[str]:
        """Extract key points from a document."""
        text = doc.full_text
        sentences = self._split_sentences(text)
        scored = self._score_sentences(sentences)
        points: list[str] = []
        for sentence, _ in scored[:max_points]:
            clean = sentence.strip()
            if clean and len(clean) > 20:
                points.append(clean)
        return points

    def compare_documents(
        self, doc_a: GovernmentDocument, doc_b: GovernmentDocument
    ) -> str:
        """Generate a brief comparison of two documents."""
        summary_a = self._extractive_summarize(doc_a, 2)
        summary_b = self._extractive_summarize(doc_b, 2)

        common_tags = set(doc_a.tags) & set(doc_b.tags)
        unique_a = set(doc_a.tags) - set(doc_b.tags)
        unique_b = set(doc_b.tags) - set(doc_a.tags)

        parts = [
            f"Document A ({doc_a.doc_id}): {doc_a.title}",
            f"  Summary: {summary_a}",
            f"Document B ({doc_b.doc_id}): {doc_b.title}",
            f"  Summary: {summary_b}",
            f"Common topics: {', '.join(common_tags) if common_tags else 'none'}",
        ]
        if unique_a:
            parts.append(f"Unique to A: {', '.join(unique_a)}")
        if unique_b:
            parts.append(f"Unique to B: {', '.join(unique_b)}")
        return "\n".join(parts)

    def _extractive_summarize(
        self, doc: GovernmentDocument, max_sentences: int
    ) -> str:
        """Score and select top sentences from the document."""
        text = doc.full_text
        sentences = self._split_sentences(text)
        if len(sentences) <= max_sentences:
            return text.strip()

        scored = self._score_sentences(sentences)
        # Pick top sentences, return in original order
        top_indices = sorted(
            [i for i, _ in scored[:max_sentences]]
        )
        selected = [sentences[i] for i in top_indices]
        return " ".join(s.strip() for s in selected)

    def _score_sentences(
        self, sentences: list[str]
    ) -> list[tuple[int, float]]:
        """Score sentences by term frequency and position.

        Returns list of (index, score) sorted by score descending.
        """
        # Build word frequency from all sentences
        all_words: list[str] = []
        for s in sentences:
            all_words.extend(self._tokenize(s))
        freq = Counter(all_words)

        scored: list[tuple[int, float]] = []
        for i, sentence in enumerate(sentences):
            words = self._tokenize(sentence)
            if not words:
                scored.append((i, 0.0))
                continue
            # TF score
            word_score = sum(freq[w] for w in words) / len(words)
            # Position bonus: first and last sentences score higher
            position_bonus = 1.0
            if i < 3:
                position_bonus = 1.5
            elif i >= len(sentences) - 2:
                position_bonus = 1.2
            # Length penalty for very short sentences
            length_factor = min(len(words) / 5, 1.0)
            score = word_score * position_bonus * length_factor
            scored.append((i, score))

        scored.sort(key=lambda x: x[1], reverse=True)
        return scored

    @staticmethod
    def _split_sentences(text: str) -> list[str]:
        """Split text into sentences."""
        sentences = re.split(r"(?<=[.!?])\s+", text)
        return [s for s in sentences if s.strip()]

    @staticmethod
    def _tokenize(text: str) -> list[str]:
        """Simple word tokenization with stopword removal."""
        stopwords = {
            "the", "a", "an", "is", "are", "was", "were", "be", "been",
            "being", "have", "has", "had", "do", "does", "did", "will",
            "would", "could", "should", "may", "might", "shall", "can",
            "of", "in", "to", "for", "with", "on", "at", "by", "from",
            "as", "into", "through", "and", "or", "but", "not", "no",
            "this", "that", "these", "those", "it", "its",
        }
        words = re.findall(r"\b[a-z]+\b", text.lower())
        return [w for w in words if w not in stopwords and len(w) > 2]

    def _llm_summarize(self, doc: GovernmentDocument) -> str:
        """Placeholder for LLM-based abstractive summarization.

        In production, this would call an LLM API. Currently returns
        the extractive summary with a note.
        """
        extractive = self._extractive_summarize(doc, 5)
        return (
            f"[LLM summary not available - API integration pending]\n"
            f"Extractive summary: {extractive}"
        )
