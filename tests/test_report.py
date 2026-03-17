"""Tests for report generation."""

from govsearch.analyzer.citation import CitationTracker
from govsearch.analyzer.summarizer import DocumentSummarizer
from govsearch.analyzer.timeline import TimelineBuilder
from govsearch.documents.database import DocumentDatabase
from govsearch.models import SearchResult
from govsearch.report import ReportGenerator
from govsearch.search.engine import SearchEngine


class TestReportGenerator:
    def setup_method(self):
        self.db = DocumentDatabase(load_samples=True)
        all_docs = self.db.all_documents()
        self.generator = ReportGenerator(
            summarizer=DocumentSummarizer(),
            citation_tracker=CitationTracker(all_docs),
            timeline_builder=TimelineBuilder(all_docs),
        )

    def test_document_report(self):
        doc = self.db.get("LEG-001")
        report = self.generator.generate_document_report(doc)
        assert report.title
        assert report.summary
        assert len(report.sections) >= 3

    def test_search_report(self):
        engine = SearchEngine(database=self.db)
        results = engine.search_text("environmental")
        report = self.generator.generate_search_report("environmental", results)
        assert "environmental" in report.title.lower()
        assert len(report.sections) >= 1

    def test_markdown_format(self):
        doc = self.db.get("LEG-001")
        report = self.generator.generate_document_report(doc)
        md = self.generator.format_report_markdown(report)
        assert md.startswith("# ")
        assert "## Summary" in md

    def test_text_format(self):
        doc = self.db.get("LEG-001")
        report = self.generator.generate_document_report(doc)
        text = self.generator.format_report_text(report)
        assert "SUMMARY" in text
        assert "===" in text

    def test_empty_search_report(self):
        report = self.generator.generate_search_report("nonexistent", [])
        assert "no results" in report.summary.lower()
