"""Tests for Pydantic data models."""

from datetime import date

from govsearch.documents.types import DocumentType, Jurisdiction
from govsearch.models import (
    Citation,
    DocumentSection,
    GovernmentDocument,
    SearchQuery,
    SearchResult,
    TimelineEvent,
)


class TestGovernmentDocument:
    def test_create_document(self):
        doc = GovernmentDocument(
            doc_id="TEST-001",
            title="Test Act",
            doc_type=DocumentType.LEGISLATION,
            agency="Test Agency",
            date_published=date(2024, 1, 1),
            full_text="This is the full text of the test act.",
        )
        assert doc.doc_id == "TEST-001"
        assert doc.doc_type == DocumentType.LEGISLATION
        assert doc.jurisdiction == Jurisdiction.FEDERAL

    def test_text_for_indexing(self):
        doc = GovernmentDocument(
            doc_id="TEST-002",
            title="Test Document",
            doc_type=DocumentType.REPORT,
            agency="Agency",
            date_published=date(2024, 1, 1),
            summary="A summary.",
            full_text="Full text here.",
            tags=["tag1", "tag2"],
        )
        text = doc.text_for_indexing
        assert "Test Document" in text
        assert "A summary." in text
        assert "Full text here." in text
        assert "tag1" in text

    def test_document_defaults(self):
        doc = GovernmentDocument(
            doc_id="T",
            title="T",
            doc_type=DocumentType.BUDGET,
            agency="A",
            date_published=date(2024, 1, 1),
            full_text="text",
        )
        assert doc.sections == []
        assert doc.citations == []
        assert doc.tags == []
        assert doc.amendments == []
        assert doc.superseded_by is None


class TestSearchQuery:
    def test_default_query(self):
        q = SearchQuery(query_text="test query")
        assert q.max_results == 20
        assert q.doc_type is None
        assert q.tags == []

    def test_filtered_query(self):
        q = SearchQuery(
            query_text="environmental",
            doc_type=DocumentType.REGULATION,
            agency="EPA",
            date_from=date(2024, 1, 1),
            max_results=5,
        )
        assert q.agency == "EPA"
        assert q.max_results == 5


class TestCitation:
    def test_citation(self):
        c = Citation(
            source_doc_id="DOC-A",
            target_doc_id="DOC-B",
            target_title="Target Document",
            context="See DOC-B for details.",
        )
        assert c.source_doc_id == "DOC-A"
        assert c.target_doc_id == "DOC-B"


class TestTimelineEvent:
    def test_event(self):
        event = TimelineEvent(
            date=date(2024, 3, 15),
            doc_id="LEG-001",
            title="Clean Air Act",
            event_type="enacted",
        )
        assert event.event_type == "enacted"
        assert event.related_doc_ids == []
