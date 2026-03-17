"""Tests for search engine, indexer, and filters."""

from datetime import date

import pytest

from govsearch.documents.database import DocumentDatabase
from govsearch.documents.types import DocumentType, Jurisdiction
from govsearch.models import GovernmentDocument, SearchQuery
from govsearch.search.engine import SearchEngine
from govsearch.search.filters import SearchFilters
from govsearch.search.indexer import DocumentIndexer


class TestDocumentIndexer:
    def test_add_and_count(self):
        indexer = DocumentIndexer()
        doc = GovernmentDocument(
            doc_id="IX-001",
            title="Indexer Test",
            doc_type=DocumentType.REPORT,
            agency="Test",
            date_published=date(2024, 1, 1),
            full_text="Testing the indexer with sample content about environment.",
        )
        indexer.add_document(doc)
        assert indexer.document_count == 1

    def test_build_tfidf_matrix(self):
        indexer = DocumentIndexer()
        for i in range(3):
            indexer.add_document(
                GovernmentDocument(
                    doc_id=f"IX-{i}",
                    title=f"Doc {i}",
                    doc_type=DocumentType.REPORT,
                    agency="Test",
                    date_published=date(2024, 1, 1),
                    full_text=f"Document number {i} about testing search functionality.",
                )
            )
        matrix = indexer.tfidf_matrix
        assert matrix is not None
        assert matrix.shape[0] == 3

    def test_remove_document(self):
        indexer = DocumentIndexer()
        doc = GovernmentDocument(
            doc_id="IX-DEL",
            title="Delete Me",
            doc_type=DocumentType.REPORT,
            agency="Test",
            date_published=date(2024, 1, 1),
            full_text="Content to be removed.",
        )
        indexer.add_document(doc)
        assert indexer.remove_document("IX-DEL") is True
        assert indexer.document_count == 0

    def test_get_document(self):
        indexer = DocumentIndexer()
        doc = GovernmentDocument(
            doc_id="IX-GET",
            title="Get Test",
            doc_type=DocumentType.REPORT,
            agency="Test",
            date_published=date(2024, 1, 1),
            full_text="Retrievable content.",
        )
        indexer.add_document(doc)
        result = indexer.get_document("IX-GET")
        assert result is not None
        assert result.title == "Get Test"
        assert indexer.get_document("NOPE") is None


class TestSearchFilters:
    @pytest.fixture()
    def sample_docs(self) -> list[GovernmentDocument]:
        return [
            GovernmentDocument(
                doc_id="F-001",
                title="EPA Regulation",
                doc_type=DocumentType.REGULATION,
                agency="Environmental Protection Agency",
                jurisdiction=Jurisdiction.FEDERAL,
                date_published=date(2024, 3, 1),
                full_text="EPA regulation content.",
                tags=["environment", "air quality"],
            ),
            GovernmentDocument(
                doc_id="F-002",
                title="State Law",
                doc_type=DocumentType.LEGISLATION,
                agency="California Legislature",
                jurisdiction=Jurisdiction.STATE,
                date_published=date(2023, 6, 15),
                full_text="State legislation content.",
                tags=["privacy", "consumer protection"],
            ),
            GovernmentDocument(
                doc_id="F-003",
                title="Federal Budget",
                doc_type=DocumentType.BUDGET,
                agency="OMB",
                jurisdiction=Jurisdiction.FEDERAL,
                date_published=date(2024, 5, 1),
                full_text="Budget content.",
                tags=["budget", "spending"],
            ),
        ]

    def test_filter_by_type(self, sample_docs):
        result = SearchFilters.filter_by_type(sample_docs, DocumentType.REGULATION)
        assert len(result) == 1
        assert result[0].doc_id == "F-001"

    def test_filter_by_agency(self, sample_docs):
        result = SearchFilters.filter_by_agency(sample_docs, "EPA")
        assert len(result) == 1

    def test_filter_by_jurisdiction(self, sample_docs):
        result = SearchFilters.filter_by_jurisdiction(sample_docs, Jurisdiction.STATE)
        assert len(result) == 1
        assert result[0].doc_id == "F-002"

    def test_filter_by_date_range(self, sample_docs):
        result = SearchFilters.filter_by_date(
            sample_docs, date_from=date(2024, 1, 1)
        )
        assert len(result) == 2

    def test_filter_by_tags(self, sample_docs):
        result = SearchFilters.filter_by_tags(sample_docs, ["environment"])
        assert len(result) == 1
        assert result[0].doc_id == "F-001"

    def test_combined_filters(self, sample_docs):
        filters = SearchFilters(
            jurisdiction=Jurisdiction.FEDERAL,
            date_from=date(2024, 1, 1),
        )
        result = filters.apply(sample_docs)
        assert len(result) == 2


class TestSearchEngine:
    def test_search_returns_results(self):
        engine = SearchEngine()
        results = engine.search_text("environmental regulation air quality")
        assert len(results) > 0
        # Top result should be related to air quality or environment
        assert results[0].score > 0

    def test_search_with_type_filter(self):
        engine = SearchEngine()
        query = SearchQuery(
            query_text="cybersecurity",
            doc_type=DocumentType.LEGISLATION,
        )
        results = engine.search(query)
        assert all(r.document.doc_type == DocumentType.LEGISLATION for r in results)

    def test_search_with_agency_filter(self):
        engine = SearchEngine()
        query = SearchQuery(
            query_text="water quality",
            agency="EPA",
        )
        results = engine.search(query)
        assert all("epa" in r.document.agency.lower() or "environmental" in r.document.agency.lower() for r in results)

    def test_find_similar(self):
        engine = SearchEngine()
        similar = engine.find_similar("LEG-001")
        assert len(similar) > 0
        # Should not include the source document itself
        assert all(r.document.doc_id != "LEG-001" for r in similar)

    def test_search_no_results(self):
        engine = SearchEngine()
        results = engine.search_text("xyznonexistentterm12345")
        assert len(results) == 0

    def test_search_snippet(self):
        engine = SearchEngine()
        results = engine.search_text("PFAS contamination")
        assert len(results) > 0
        assert results[0].snippet  # Should have a snippet
