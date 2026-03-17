"""Citation tracker for finding cross-references between government documents."""

from __future__ import annotations

from collections import defaultdict

from govsearch.documents.parser import DocumentParser
from govsearch.models import Citation, GovernmentDocument


class CitationTracker:
    """Tracks cross-references and citation relationships between documents.

    Builds a citation graph from document references and provides
    queries for incoming citations, outgoing references, and
    co-citation analysis.
    """

    def __init__(self, documents: list[GovernmentDocument] | None = None) -> None:
        self._parser = DocumentParser()
        # doc_id -> list of citations from that document
        self._outgoing: dict[str, list[Citation]] = defaultdict(list)
        # doc_id -> list of citations pointing to that document
        self._incoming: dict[str, list[Citation]] = defaultdict(list)
        # All known documents
        self._documents: dict[str, GovernmentDocument] = {}
        if documents:
            self.index_documents(documents)

    def index_documents(self, documents: list[GovernmentDocument]) -> None:
        """Build citation graph from a list of documents."""
        for doc in documents:
            self._documents[doc.doc_id] = doc

        for doc in documents:
            # Use explicit citations from the document
            for cite in doc.citations:
                self._outgoing[doc.doc_id].append(cite)
                self._incoming[cite.target_doc_id].append(cite)

            # Also use related_docs references
            for related_id in doc.related_docs:
                if related_id != doc.doc_id:
                    cite = Citation(
                        source_doc_id=doc.doc_id,
                        target_doc_id=related_id,
                        target_title=self._get_title(related_id),
                        context=f"Related document reference in {doc.title}",
                    )
                    if not self._has_citation(doc.doc_id, related_id):
                        self._outgoing[doc.doc_id].append(cite)
                        self._incoming[related_id].append(cite)

            # Parse text for additional citations
            parsed_citations = self._parser.extract_citations(doc)
            for cite in parsed_citations:
                if not self._has_citation(cite.source_doc_id, cite.target_doc_id):
                    self._outgoing[cite.source_doc_id].append(cite)

    def get_outgoing_citations(self, doc_id: str) -> list[Citation]:
        """Get all citations made by a document."""
        return self._outgoing.get(doc_id, [])

    def get_incoming_citations(self, doc_id: str) -> list[Citation]:
        """Get all citations pointing to a document."""
        return self._incoming.get(doc_id, [])

    def get_citation_count(self, doc_id: str) -> dict[str, int]:
        """Get incoming and outgoing citation counts."""
        return {
            "outgoing": len(self._outgoing.get(doc_id, [])),
            "incoming": len(self._incoming.get(doc_id, [])),
        }

    def find_co_cited(self, doc_id: str) -> list[str]:
        """Find documents that are frequently cited alongside the given document.

        Returns document IDs that share citations with the query document.
        """
        # Find all docs that cite this document
        citers = {c.source_doc_id for c in self._incoming.get(doc_id, [])}

        # Find what else those documents cite
        co_cited: dict[str, int] = defaultdict(int)
        for citer_id in citers:
            for cite in self._outgoing.get(citer_id, []):
                if cite.target_doc_id != doc_id:
                    co_cited[cite.target_doc_id] += 1

        # Sort by co-citation frequency
        return sorted(co_cited.keys(), key=lambda x: co_cited[x], reverse=True)

    def get_citation_chain(
        self, doc_id: str, max_depth: int = 3
    ) -> dict[str, list[str]]:
        """Trace citation chain outward from a document.

        Returns a dict mapping depth level to document IDs at that level.
        """
        chain: dict[str, list[str]] = {}
        visited: set[str] = {doc_id}
        current_level = [doc_id]

        for depth in range(1, max_depth + 1):
            next_level: list[str] = []
            for current_id in current_level:
                for cite in self._outgoing.get(current_id, []):
                    target = cite.target_doc_id
                    if target not in visited and target in self._documents:
                        next_level.append(target)
                        visited.add(target)
            if next_level:
                chain[f"depth_{depth}"] = next_level
            current_level = next_level

        return chain

    def most_cited(self, top_n: int = 10) -> list[tuple[str, int]]:
        """Return the most-cited documents by incoming citation count."""
        counts = {
            doc_id: len(citations)
            for doc_id, citations in self._incoming.items()
        }
        return sorted(counts.items(), key=lambda x: x[1], reverse=True)[:top_n]

    def _get_title(self, doc_id: str) -> str:
        doc = self._documents.get(doc_id)
        return doc.title if doc else doc_id

    def _has_citation(self, source_id: str, target_id: str) -> bool:
        return any(
            c.target_doc_id == target_id
            for c in self._outgoing.get(source_id, [])
        )
