"""Full-text search engine with TF-IDF ranking for government documents."""

from __future__ import annotations

import re

from sklearn.metrics.pairwise import cosine_similarity

from govsearch.documents.database import DocumentDatabase
from govsearch.models import GovernmentDocument, SearchQuery, SearchResult
from govsearch.search.filters import SearchFilters
from govsearch.search.indexer import DocumentIndexer


class SearchEngine:
    """Full-text search engine using TF-IDF ranking over government documents.

    Combines TF-IDF cosine similarity scoring with structured filters
    for date, agency, document type, and jurisdiction.
    """

    def __init__(self, database: DocumentDatabase | None = None) -> None:
        self._indexer = DocumentIndexer()
        self._database = database or DocumentDatabase()
        # Index all documents from the database
        self._indexer.add_documents(self._database.all_documents())

    @property
    def indexer(self) -> DocumentIndexer:
        return self._indexer

    @property
    def database(self) -> DocumentDatabase:
        return self._database

    def search(self, query: SearchQuery) -> list[SearchResult]:
        """Execute a search query and return ranked results."""
        # Get TF-IDF ranked results
        ranked = self._tfidf_search(query.query_text)

        # Apply filters
        filters = SearchFilters(
            doc_type=query.doc_type,
            agency=query.agency,
            jurisdiction=query.jurisdiction,
            date_from=query.date_from,
            date_to=query.date_to,
            tags=query.tags,
        )

        # Filter the ranked results while preserving scores
        filtered_docs = filters.apply([r.document for r in ranked])
        filtered_ids = {d.doc_id for d in filtered_docs}
        results = [r for r in ranked if r.document.doc_id in filtered_ids]

        return results[: query.max_results]

    def search_text(
        self, query_text: str, max_results: int = 20
    ) -> list[SearchResult]:
        """Simple text search without additional filters."""
        query = SearchQuery(query_text=query_text, max_results=max_results)
        return self.search(query)

    def find_similar(
        self, doc_id: str, max_results: int = 10
    ) -> list[SearchResult]:
        """Find documents similar to the given document."""
        doc = self._indexer.get_document(doc_id)
        if doc is None:
            return []
        results = self._tfidf_search(doc.text_for_indexing)
        # Exclude the query document itself
        return [r for r in results if r.document.doc_id != doc_id][:max_results]

    def add_document(self, doc: GovernmentDocument) -> None:
        """Add a document to both the database and search index."""
        self._database.add(doc)
        self._indexer.add_document(doc)

    def _tfidf_search(self, query_text: str) -> list[SearchResult]:
        """Perform TF-IDF cosine similarity search."""
        matrix = self._indexer.tfidf_matrix
        if matrix is None:
            return []

        query_vec = self._indexer.vectorizer.transform([query_text])
        similarities = cosine_similarity(query_vec, matrix).flatten()

        # Build results sorted by score descending
        results: list[SearchResult] = []
        documents = self._indexer.get_all_documents()
        scored = sorted(
            enumerate(similarities), key=lambda x: x[1], reverse=True
        )

        for idx, score in scored:
            if score <= 0.0:
                continue
            doc = documents[idx]
            snippet = self._extract_snippet(doc, query_text)
            matched = self._find_matched_sections(doc, query_text)
            results.append(
                SearchResult(
                    document=doc,
                    score=round(float(score), 4),
                    snippet=snippet,
                    matched_sections=matched,
                )
            )
        return results

    @staticmethod
    def _extract_snippet(doc: GovernmentDocument, query: str) -> str:
        """Extract a text snippet around the first query term match."""
        terms = query.lower().split()
        text = doc.full_text
        text_lower = text.lower()

        for term in terms:
            pos = text_lower.find(term)
            if pos >= 0:
                start = max(0, pos - 60)
                end = min(len(text), pos + len(term) + 120)
                snippet = text[start:end].strip()
                if start > 0:
                    snippet = "..." + snippet
                if end < len(text):
                    snippet = snippet + "..."
                return snippet
        return doc.summary[:200] if doc.summary else doc.full_text[:200]

    @staticmethod
    def _find_matched_sections(
        doc: GovernmentDocument, query: str
    ) -> list[str]:
        """Find section numbers where query terms appear."""
        terms = query.lower().split()
        matched: list[str] = []
        for section in doc.sections:
            content_lower = (section.title + " " + section.content).lower()
            if any(term in content_lower for term in terms):
                label = f"Section {section.number}"
                if section.title:
                    label += f": {section.title}"
                matched.append(label)
        return matched
