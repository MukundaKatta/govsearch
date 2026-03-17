"""Pydantic data models for GOVSEARCH."""

from __future__ import annotations

from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field

from govsearch.documents.types import DocumentStatus, DocumentType, Jurisdiction


class Citation(BaseModel):
    """A reference from one document to another."""

    source_doc_id: str = Field(description="ID of the citing document")
    target_doc_id: str = Field(description="ID of the cited document")
    target_title: str = Field(default="", description="Title of the cited document")
    context: str = Field(default="", description="Surrounding text of the citation")
    section: str = Field(default="", description="Section where citation appears")


class DocumentSection(BaseModel):
    """A named section within a government document."""

    number: str = Field(description="Section number or identifier")
    title: str = Field(default="", description="Section heading")
    content: str = Field(description="Section body text")
    subsections: list[DocumentSection] = Field(default_factory=list)


class GovernmentDocument(BaseModel):
    """Core model representing a government document."""

    doc_id: str = Field(description="Unique document identifier")
    title: str = Field(description="Document title")
    doc_type: DocumentType = Field(description="Type of government document")
    agency: str = Field(description="Issuing government agency")
    jurisdiction: Jurisdiction = Field(default=Jurisdiction.FEDERAL)
    status: DocumentStatus = Field(default=DocumentStatus.ACTIVE)
    date_published: date = Field(description="Publication date")
    date_effective: Optional[date] = Field(default=None)
    date_expires: Optional[date] = Field(default=None)
    summary: str = Field(default="", description="Brief summary")
    full_text: str = Field(description="Complete document text")
    sections: list[DocumentSection] = Field(default_factory=list)
    citations: list[Citation] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)
    amendments: list[str] = Field(
        default_factory=list, description="IDs of amending documents"
    )
    superseded_by: Optional[str] = Field(default=None)
    related_docs: list[str] = Field(default_factory=list)

    @property
    def text_for_indexing(self) -> str:
        """Combined text used for search indexing."""
        parts = [self.title, self.summary, self.full_text]
        parts.extend(self.tags)
        for section in self.sections:
            parts.append(section.title)
            parts.append(section.content)
        return " ".join(parts)


class SearchResult(BaseModel):
    """A single search result with relevance score."""

    document: GovernmentDocument
    score: float = Field(description="TF-IDF relevance score", ge=0.0)
    matched_sections: list[str] = Field(default_factory=list)
    snippet: str = Field(default="", description="Highlighted text snippet")


class SearchQuery(BaseModel):
    """Structured search query with filters."""

    query_text: str = Field(description="Free-text search query")
    doc_type: Optional[DocumentType] = Field(default=None)
    agency: Optional[str] = Field(default=None)
    jurisdiction: Optional[Jurisdiction] = Field(default=None)
    date_from: Optional[date] = Field(default=None)
    date_to: Optional[date] = Field(default=None)
    tags: list[str] = Field(default_factory=list)
    max_results: int = Field(default=20, ge=1, le=100)


class TimelineEvent(BaseModel):
    """An event in a document's legislative/regulatory history."""

    date: date
    doc_id: str
    title: str
    event_type: str = Field(description="e.g., 'enacted', 'amended', 'repealed'")
    description: str = Field(default="")
    related_doc_ids: list[str] = Field(default_factory=list)


class DocumentReport(BaseModel):
    """A generated report about a document or search results."""

    title: str
    generated_at: datetime = Field(default_factory=datetime.now)
    summary: str
    sections: list[DocumentSection] = Field(default_factory=list)
    documents_referenced: list[str] = Field(default_factory=list)
    citation_count: int = Field(default=0)
    timeline: list[TimelineEvent] = Field(default_factory=list)
