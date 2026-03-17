"""Search filters for narrowing government document results."""

from __future__ import annotations

from datetime import date

from govsearch.documents.types import DocumentType, Jurisdiction
from govsearch.models import GovernmentDocument


class SearchFilters:
    """Composable filters for government document search results.

    Filters can be applied individually or combined. Each filter method
    returns a new filtered list, allowing chaining.
    """

    def __init__(
        self,
        doc_type: DocumentType | None = None,
        agency: str | None = None,
        jurisdiction: Jurisdiction | None = None,
        date_from: date | None = None,
        date_to: date | None = None,
        tags: list[str] | None = None,
        status: str | None = None,
    ) -> None:
        self.doc_type = doc_type
        self.agency = agency
        self.jurisdiction = jurisdiction
        self.date_from = date_from
        self.date_to = date_to
        self.tags = tags or []
        self.status = status

    def apply(self, documents: list[GovernmentDocument]) -> list[GovernmentDocument]:
        """Apply all configured filters to a list of documents."""
        result = documents
        if self.doc_type is not None:
            result = self.filter_by_type(result, self.doc_type)
        if self.agency is not None:
            result = self.filter_by_agency(result, self.agency)
        if self.jurisdiction is not None:
            result = self.filter_by_jurisdiction(result, self.jurisdiction)
        if self.date_from is not None or self.date_to is not None:
            result = self.filter_by_date(result, self.date_from, self.date_to)
        if self.tags:
            result = self.filter_by_tags(result, self.tags)
        if self.status is not None:
            result = self.filter_by_status(result, self.status)
        return result

    @staticmethod
    def filter_by_type(
        documents: list[GovernmentDocument], doc_type: DocumentType
    ) -> list[GovernmentDocument]:
        """Filter documents by document type."""
        return [d for d in documents if d.doc_type == doc_type]

    @staticmethod
    def filter_by_agency(
        documents: list[GovernmentDocument], agency: str
    ) -> list[GovernmentDocument]:
        """Filter documents by issuing agency (case-insensitive substring match)."""
        agency_lower = agency.lower()
        return [d for d in documents if agency_lower in d.agency.lower()]

    @staticmethod
    def filter_by_jurisdiction(
        documents: list[GovernmentDocument], jurisdiction: Jurisdiction
    ) -> list[GovernmentDocument]:
        """Filter documents by jurisdiction level."""
        return [d for d in documents if d.jurisdiction == jurisdiction]

    @staticmethod
    def filter_by_date(
        documents: list[GovernmentDocument],
        date_from: date | None = None,
        date_to: date | None = None,
    ) -> list[GovernmentDocument]:
        """Filter documents by publication date range."""
        result = documents
        if date_from is not None:
            result = [d for d in result if d.date_published >= date_from]
        if date_to is not None:
            result = [d for d in result if d.date_published <= date_to]
        return result

    @staticmethod
    def filter_by_tags(
        documents: list[GovernmentDocument],
        tags: list[str],
        match_all: bool = False,
    ) -> list[GovernmentDocument]:
        """Filter documents that have any (or all) of the specified tags."""
        tag_set = {t.lower() for t in tags}
        results = []
        for doc in documents:
            doc_tags = {t.lower() for t in doc.tags}
            if match_all:
                if tag_set.issubset(doc_tags):
                    results.append(doc)
            else:
                if tag_set & doc_tags:
                    results.append(doc)
        return results

    @staticmethod
    def filter_by_status(
        documents: list[GovernmentDocument], status: str
    ) -> list[GovernmentDocument]:
        """Filter documents by lifecycle status."""
        status_lower = status.lower()
        return [d for d in documents if d.status.value.lower() == status_lower]
