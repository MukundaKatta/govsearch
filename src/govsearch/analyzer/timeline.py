"""Timeline builder for document legislative/regulatory history."""

from __future__ import annotations

from collections import defaultdict

from govsearch.documents.types import DocumentStatus
from govsearch.models import GovernmentDocument, TimelineEvent


class TimelineBuilder:
    """Builds chronological timelines showing document history and relationships.

    Traces the evolution of legislation, regulations, and related documents
    through amendments, supersessions, and cross-references.
    """

    def __init__(self, documents: list[GovernmentDocument] | None = None) -> None:
        self._documents: dict[str, GovernmentDocument] = {}
        if documents:
            for doc in documents:
                self._documents[doc.doc_id] = doc

    def add_documents(self, documents: list[GovernmentDocument]) -> None:
        """Add documents to the timeline builder."""
        for doc in documents:
            self._documents[doc.doc_id] = doc

    def build_timeline(self, doc_id: str) -> list[TimelineEvent]:
        """Build a timeline for a document and its related documents.

        Traces the document's history through publication, amendments,
        related documents, and status changes.
        """
        root = self._documents.get(doc_id)
        if root is None:
            return []

        events: list[TimelineEvent] = []

        # Add the root document's publication
        events.append(
            TimelineEvent(
                date=root.date_published,
                doc_id=root.doc_id,
                title=root.title,
                event_type=self._infer_event_type(root),
                description=root.summary,
            )
        )

        # Add effective date if different from publication
        if root.date_effective and root.date_effective != root.date_published:
            events.append(
                TimelineEvent(
                    date=root.date_effective,
                    doc_id=root.doc_id,
                    title=root.title,
                    event_type="effective",
                    description=f"{root.title} takes effect.",
                )
            )

        # Add expiration date
        if root.date_expires:
            events.append(
                TimelineEvent(
                    date=root.date_expires,
                    doc_id=root.doc_id,
                    title=root.title,
                    event_type="expired",
                    description=f"{root.title} expires.",
                )
            )

        # Add related documents
        related_ids = set(root.related_docs + root.amendments)
        if root.superseded_by:
            related_ids.add(root.superseded_by)

        for related_id in related_ids:
            related = self._documents.get(related_id)
            if related is None:
                continue
            events.append(
                TimelineEvent(
                    date=related.date_published,
                    doc_id=related.doc_id,
                    title=related.title,
                    event_type=self._infer_relationship(root, related),
                    description=related.summary,
                    related_doc_ids=[root.doc_id],
                )
            )

        # Sort by date
        events.sort(key=lambda e: e.date)
        return events

    def build_topic_timeline(self, topic: str) -> list[TimelineEvent]:
        """Build a timeline of all documents related to a topic.

        Searches document titles, summaries, and tags for the topic.
        """
        topic_lower = topic.lower()
        matching_docs: list[GovernmentDocument] = []

        for doc in self._documents.values():
            if (
                topic_lower in doc.title.lower()
                or topic_lower in doc.summary.lower()
                or any(topic_lower in tag.lower() for tag in doc.tags)
            ):
                matching_docs.append(doc)

        events: list[TimelineEvent] = []
        for doc in matching_docs:
            events.append(
                TimelineEvent(
                    date=doc.date_published,
                    doc_id=doc.doc_id,
                    title=doc.title,
                    event_type=self._infer_event_type(doc),
                    description=doc.summary,
                )
            )

        events.sort(key=lambda e: e.date)
        return events

    def get_document_lineage(self, doc_id: str) -> list[str]:
        """Trace the full lineage of a document through amendments and supersessions.

        Returns an ordered list of document IDs from oldest ancestor to newest.
        """
        lineage: list[str] = []
        visited: set[str] = set()
        self._trace_backwards(doc_id, lineage, visited)
        lineage.reverse()
        self._trace_forwards(doc_id, lineage, visited)
        return lineage

    def _trace_backwards(
        self, doc_id: str, lineage: list[str], visited: set[str]
    ) -> None:
        """Trace backwards through supersession chain."""
        if doc_id in visited:
            return
        visited.add(doc_id)
        lineage.append(doc_id)
        # Find documents that this one superseded
        for doc in self._documents.values():
            if doc.superseded_by == doc_id:
                self._trace_backwards(doc.doc_id, lineage, visited)

    def _trace_forwards(
        self, doc_id: str, lineage: list[str], visited: set[str]
    ) -> None:
        """Trace forwards through supersession chain."""
        doc = self._documents.get(doc_id)
        if doc is None:
            return
        if doc.superseded_by and doc.superseded_by not in visited:
            visited.add(doc.superseded_by)
            lineage.append(doc.superseded_by)
            self._trace_forwards(doc.superseded_by, lineage, visited)

    @staticmethod
    def _infer_event_type(doc: GovernmentDocument) -> str:
        """Infer the event type from a document's type and status."""
        type_map = {
            "legislation": "enacted",
            "regulation": "promulgated",
            "court_ruling": "decided",
            "executive_order": "signed",
            "budget": "submitted",
            "report": "published",
        }
        if doc.status == DocumentStatus.PROPOSED:
            return "proposed"
        if doc.status == DocumentStatus.REPEALED:
            return "repealed"
        if doc.status == DocumentStatus.AMENDED:
            return "amended"
        return type_map.get(doc.doc_type.value, "published")

    @staticmethod
    def _infer_relationship(
        root: GovernmentDocument, related: GovernmentDocument
    ) -> str:
        """Infer the relationship type between two documents."""
        if related.doc_id in root.amendments:
            return "amendment"
        if root.superseded_by == related.doc_id:
            return "superseded_by"
        if related.doc_type.value == "regulation":
            return "implementing_regulation"
        if related.doc_type.value == "court_ruling":
            return "judicial_review"
        if related.doc_type.value == "report":
            return "supporting_report"
        if related.doc_type.value == "executive_order":
            return "executive_directive"
        return "related"
