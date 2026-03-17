"""Tests for analyzer components: summarizer, citations, timeline."""

from datetime import date

from govsearch.analyzer.citation import CitationTracker
from govsearch.analyzer.summarizer import DocumentSummarizer
from govsearch.analyzer.timeline import TimelineBuilder
from govsearch.documents.database import DocumentDatabase
from govsearch.documents.types import DocumentType
from govsearch.models import Citation, GovernmentDocument


class TestDocumentSummarizer:
    def setup_method(self):
        self.summarizer = DocumentSummarizer()

    def test_summarize_short_document(self):
        doc = GovernmentDocument(
            doc_id="S-001",
            title="Short Doc",
            doc_type=DocumentType.REPORT,
            agency="Test",
            date_published=date(2024, 1, 1),
            full_text="This is a short document. It only has two sentences.",
        )
        summary = self.summarizer.summarize(doc, max_sentences=5)
        assert len(summary) > 0

    def test_summarize_long_document(self):
        db = DocumentDatabase(load_samples=True)
        doc = db.get("LEG-001")
        summary = self.summarizer.summarize(doc, max_sentences=3)
        assert len(summary) > 0
        assert len(summary) < len(doc.full_text)

    def test_key_points(self):
        db = DocumentDatabase(load_samples=True)
        doc = db.get("LEG-001")
        points = self.summarizer.key_points(doc, max_points=3)
        assert len(points) > 0
        assert len(points) <= 3

    def test_compare_documents(self):
        db = DocumentDatabase(load_samples=True)
        doc_a = db.get("LEG-001")
        doc_b = db.get("REG-001")
        comparison = self.summarizer.compare_documents(doc_a, doc_b)
        assert "LEG-001" in comparison
        assert "REG-001" in comparison

    def test_llm_fallback(self):
        summarizer = DocumentSummarizer(llm_api_key="fake-key")
        doc = GovernmentDocument(
            doc_id="S-002",
            title="LLM Test",
            doc_type=DocumentType.REPORT,
            agency="Test",
            date_published=date(2024, 1, 1),
            full_text="A document for testing LLM summarization fallback behavior.",
        )
        result = summarizer.summarize(doc, use_llm=True)
        assert "LLM summary not available" in result


class TestCitationTracker:
    def test_outgoing_citations(self):
        db = DocumentDatabase(load_samples=True)
        tracker = CitationTracker(db.all_documents())
        outgoing = tracker.get_outgoing_citations("LEG-001")
        assert len(outgoing) > 0

    def test_incoming_citations(self):
        db = DocumentDatabase(load_samples=True)
        tracker = CitationTracker(db.all_documents())
        # REG-001 should be referenced by LEG-001
        incoming = tracker.get_incoming_citations("REG-001")
        assert len(incoming) > 0

    def test_citation_count(self):
        db = DocumentDatabase(load_samples=True)
        tracker = CitationTracker(db.all_documents())
        counts = tracker.get_citation_count("LEG-001")
        assert "outgoing" in counts
        assert "incoming" in counts
        assert counts["outgoing"] >= 0

    def test_most_cited(self):
        db = DocumentDatabase(load_samples=True)
        tracker = CitationTracker(db.all_documents())
        most = tracker.most_cited(5)
        assert len(most) > 0
        # Should be sorted by count descending
        if len(most) > 1:
            assert most[0][1] >= most[1][1]

    def test_citation_chain(self):
        db = DocumentDatabase(load_samples=True)
        tracker = CitationTracker(db.all_documents())
        chain = tracker.get_citation_chain("LEG-001", max_depth=2)
        assert isinstance(chain, dict)

    def test_find_co_cited(self):
        db = DocumentDatabase(load_samples=True)
        tracker = CitationTracker(db.all_documents())
        co_cited = tracker.find_co_cited("LEG-001")
        assert isinstance(co_cited, list)


class TestTimelineBuilder:
    def test_document_timeline(self):
        db = DocumentDatabase(load_samples=True)
        builder = TimelineBuilder(db.all_documents())
        events = builder.build_timeline("LEG-001")
        assert len(events) > 0
        # Events should be sorted by date
        for i in range(len(events) - 1):
            assert events[i].date <= events[i + 1].date

    def test_topic_timeline(self):
        db = DocumentDatabase(load_samples=True)
        builder = TimelineBuilder(db.all_documents())
        events = builder.build_topic_timeline("cybersecurity")
        assert len(events) > 0

    def test_topic_timeline_no_results(self):
        db = DocumentDatabase(load_samples=True)
        builder = TimelineBuilder(db.all_documents())
        events = builder.build_topic_timeline("xyznonexistent")
        assert len(events) == 0

    def test_nonexistent_document(self):
        builder = TimelineBuilder()
        events = builder.build_timeline("NOPE")
        assert events == []

    def test_document_lineage(self):
        db = DocumentDatabase(load_samples=True)
        builder = TimelineBuilder(db.all_documents())
        lineage = builder.get_document_lineage("LEG-001")
        assert "LEG-001" in lineage
