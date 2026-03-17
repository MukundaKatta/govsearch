"""Report generation for government document analysis."""

from __future__ import annotations

from datetime import datetime

from govsearch.analyzer.citation import CitationTracker
from govsearch.analyzer.summarizer import DocumentSummarizer
from govsearch.analyzer.timeline import TimelineBuilder
from govsearch.models import (
    DocumentReport,
    DocumentSection,
    GovernmentDocument,
    SearchResult,
    TimelineEvent,
)


class ReportGenerator:
    """Generates structured reports about government documents.

    Combines summarization, citation analysis, and timeline data
    into comprehensive document reports.
    """

    def __init__(
        self,
        summarizer: DocumentSummarizer | None = None,
        citation_tracker: CitationTracker | None = None,
        timeline_builder: TimelineBuilder | None = None,
    ) -> None:
        self._summarizer = summarizer or DocumentSummarizer()
        self._citation_tracker = citation_tracker
        self._timeline_builder = timeline_builder

    def generate_document_report(
        self, doc: GovernmentDocument
    ) -> DocumentReport:
        """Generate a comprehensive report for a single document."""
        summary = self._summarizer.summarize(doc)
        key_points = self._summarizer.key_points(doc)

        sections = [
            DocumentSection(
                number="1",
                title="Overview",
                content=(
                    f"Title: {doc.title}\n"
                    f"Type: {doc.doc_type.display_name}\n"
                    f"Agency: {doc.agency}\n"
                    f"Published: {doc.date_published}\n"
                    f"Status: {doc.status.value}\n"
                    f"Jurisdiction: {doc.jurisdiction.value}"
                ),
            ),
            DocumentSection(
                number="2",
                title="Summary",
                content=summary,
            ),
            DocumentSection(
                number="3",
                title="Key Points",
                content="\n".join(f"- {p}" for p in key_points),
            ),
        ]

        # Citation analysis
        citation_count = 0
        docs_referenced: list[str] = []
        if self._citation_tracker:
            outgoing = self._citation_tracker.get_outgoing_citations(doc.doc_id)
            incoming = self._citation_tracker.get_incoming_citations(doc.doc_id)
            citation_count = len(outgoing) + len(incoming)
            docs_referenced = [c.target_doc_id for c in outgoing]

            sections.append(
                DocumentSection(
                    number="4",
                    title="Citations",
                    content=(
                        f"Outgoing references: {len(outgoing)}\n"
                        f"Incoming citations: {len(incoming)}\n"
                        f"Referenced documents: {', '.join(docs_referenced) or 'none'}"
                    ),
                )
            )

        # Timeline
        timeline: list[TimelineEvent] = []
        if self._timeline_builder:
            timeline = self._timeline_builder.build_timeline(doc.doc_id)
            if timeline:
                timeline_text = "\n".join(
                    f"- {e.date}: {e.event_type} - {e.title}"
                    for e in timeline
                )
                sections.append(
                    DocumentSection(
                        number="5",
                        title="Timeline",
                        content=timeline_text,
                    )
                )

        return DocumentReport(
            title=f"Report: {doc.title}",
            generated_at=datetime.now(),
            summary=summary,
            sections=sections,
            documents_referenced=docs_referenced,
            citation_count=citation_count,
            timeline=timeline,
        )

    def generate_search_report(
        self, query: str, results: list[SearchResult]
    ) -> DocumentReport:
        """Generate a report summarizing search results."""
        sections = [
            DocumentSection(
                number="1",
                title="Search Query",
                content=f'Query: "{query}"\nResults found: {len(results)}',
            ),
        ]

        for i, result in enumerate(results[:10], 2):
            doc = result.document
            sections.append(
                DocumentSection(
                    number=str(i),
                    title=f"[{doc.doc_id}] {doc.title}",
                    content=(
                        f"Score: {result.score:.4f}\n"
                        f"Type: {doc.doc_type.display_name}\n"
                        f"Agency: {doc.agency}\n"
                        f"Date: {doc.date_published}\n"
                        f"Snippet: {result.snippet}"
                    ),
                )
            )

        summary = (
            f"Search for '{query}' returned {len(results)} results. "
            f"Top result: {results[0].document.title} "
            f"(score: {results[0].score:.4f})"
            if results
            else f"Search for '{query}' returned no results."
        )

        return DocumentReport(
            title=f"Search Report: {query}",
            generated_at=datetime.now(),
            summary=summary,
            sections=sections,
            documents_referenced=[r.document.doc_id for r in results[:10]],
        )

    def format_report_markdown(self, report: DocumentReport) -> str:
        """Format a report as Markdown text."""
        lines = [
            f"# {report.title}",
            f"*Generated: {report.generated_at:%Y-%m-%d %H:%M}*",
            "",
            f"## Summary",
            report.summary,
            "",
        ]
        for section in report.sections:
            title = section.title or f"Section {section.number}"
            lines.append(f"## {section.number}. {title}")
            lines.append(section.content)
            lines.append("")

        if report.timeline:
            lines.append("## Timeline")
            for event in report.timeline:
                lines.append(f"- **{event.date}** [{event.event_type}] {event.title}")
            lines.append("")

        return "\n".join(lines)

    def format_report_text(self, report: DocumentReport) -> str:
        """Format a report as plain text."""
        lines = [
            report.title.upper(),
            "=" * len(report.title),
            f"Generated: {report.generated_at:%Y-%m-%d %H:%M}",
            "",
            "SUMMARY",
            "-" * 40,
            report.summary,
            "",
        ]
        for section in report.sections:
            title = section.title or f"Section {section.number}"
            lines.append(f"{section.number}. {title}")
            lines.append("-" * 40)
            lines.append(section.content)
            lines.append("")

        return "\n".join(lines)
