"""Document parser for extracting structure from government documents."""

from __future__ import annotations

import re
from datetime import date

from govsearch.models import Citation, DocumentSection, GovernmentDocument


class DocumentParser:
    """Extracts sections, citations, and dates from government documents."""

    # Patterns for section headers in government documents
    SECTION_PATTERNS = [
        re.compile(
            r"^(?:SEC(?:TION)?\.?\s*)(\d+[A-Za-z]?(?:\.\d+)*)\s*[.\-\s]*(.*)$",
            re.MULTILINE,
        ),
        re.compile(
            r"^(?:ARTICLE|Art\.)\s+([IVXLCDM]+|\d+)\s*[.\-\s]*(.*)$",
            re.MULTILINE,
        ),
        re.compile(
            r"^(?:TITLE|Title)\s+([IVXLCDM]+|\d+)\s*[.\-\s]*(.*)$",
            re.MULTILINE,
        ),
        re.compile(
            r"^\(([a-z]|\d+)\)\s+(.*)$",
            re.MULTILINE,
        ),
    ]

    # Patterns for citations to other documents
    CITATION_PATTERNS = [
        re.compile(r"(\d+)\s+U\.?S\.?C\.?\s+(?:Sec(?:tion|\.)\s*)?(\d+)"),
        re.compile(r"(\d+)\s+C\.?F\.?R\.?\s+(?:Part\s+)?(\d+(?:\.\d+)*)"),
        re.compile(r"Pub(?:lic)?\.?\s*L(?:aw)?\.?\s*(\d+)[-\s](\d+)"),
        re.compile(r"(?:Executive Order|E\.O\.)\s+(\d+)"),
        re.compile(r"(\d+)\s+Stat\.?\s+(\d+)"),
        re.compile(r"(\d+)\s+F(?:ed)?\.?\s*(?:Supp|App)\.?\s*(?:\d*d?\s+)?(\d+)"),
        re.compile(r"(?:H\.?R\.?|S\.?)\s*(\d+)"),
    ]

    # Date patterns
    DATE_PATTERNS = [
        re.compile(
            r"(?:January|February|March|April|May|June|July|August|"
            r"September|October|November|December)\s+\d{1,2},?\s+\d{4}"
        ),
        re.compile(r"\d{1,2}/\d{1,2}/\d{4}"),
        re.compile(r"\d{4}-\d{2}-\d{2}"),
    ]

    MONTH_MAP = {
        "january": 1, "february": 2, "march": 3, "april": 4,
        "may": 5, "june": 6, "july": 7, "august": 8,
        "september": 9, "october": 10, "november": 11, "december": 12,
    }

    def extract_sections(self, text: str) -> list[DocumentSection]:
        """Extract structured sections from document text."""
        sections: list[DocumentSection] = []
        # Try each section pattern and use the one that finds matches
        for pattern in self.SECTION_PATTERNS:
            matches = list(pattern.finditer(text))
            if len(matches) >= 2:
                for i, match in enumerate(matches):
                    start = match.end()
                    end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
                    content = text[start:end].strip()
                    sections.append(
                        DocumentSection(
                            number=match.group(1),
                            title=match.group(2).strip() if match.lastindex >= 2 else "",
                            content=content[:2000],
                        )
                    )
                break

        if not sections and len(text) > 100:
            # Fall back to paragraph-based splitting
            paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
            for i, para in enumerate(paragraphs[:20], 1):
                sections.append(
                    DocumentSection(
                        number=str(i),
                        title="",
                        content=para[:2000],
                    )
                )
        return sections

    def extract_citations(
        self, doc: GovernmentDocument, all_doc_ids: list[str] | None = None
    ) -> list[Citation]:
        """Extract citations and cross-references from document text."""
        citations: list[Citation] = []
        seen: set[str] = set()

        for pattern in self.CITATION_PATTERNS:
            for match in pattern.finditer(doc.full_text):
                ref_text = match.group(0)
                if ref_text in seen:
                    continue
                seen.add(ref_text)

                # Find surrounding context
                start = max(0, match.start() - 80)
                end = min(len(doc.full_text), match.end() + 80)
                context = doc.full_text[start:end].strip()

                citations.append(
                    Citation(
                        source_doc_id=doc.doc_id,
                        target_doc_id=ref_text,
                        target_title=ref_text,
                        context=context,
                        section=self._find_section_for_position(
                            doc, match.start()
                        ),
                    )
                )
        return citations

    def extract_dates(self, text: str) -> list[date]:
        """Extract all dates mentioned in the document text."""
        dates: list[date] = []
        for pattern in self.DATE_PATTERNS:
            for match in pattern.finditer(text):
                parsed = self._parse_date_string(match.group(0))
                if parsed and parsed not in dates:
                    dates.append(parsed)
        return sorted(dates)

    def _parse_date_string(self, s: str) -> date | None:
        """Parse a date string into a date object."""
        s = s.strip().replace(",", "")
        # ISO format: 2024-01-15
        iso_match = re.match(r"(\d{4})-(\d{2})-(\d{2})", s)
        if iso_match:
            try:
                return date(
                    int(iso_match.group(1)),
                    int(iso_match.group(2)),
                    int(iso_match.group(3)),
                )
            except ValueError:
                return None

        # US format: 1/15/2024
        us_match = re.match(r"(\d{1,2})/(\d{1,2})/(\d{4})", s)
        if us_match:
            try:
                return date(
                    int(us_match.group(3)),
                    int(us_match.group(1)),
                    int(us_match.group(2)),
                )
            except ValueError:
                return None

        # Written: January 15 2024
        for month_name, month_num in self.MONTH_MAP.items():
            pattern = re.compile(
                rf"{month_name}\s+(\d{{1,2}})\s+(\d{{4}})", re.IGNORECASE
            )
            m = pattern.match(s)
            if m:
                try:
                    return date(int(m.group(2)), month_num, int(m.group(1)))
                except ValueError:
                    return None
        return None

    def _find_section_for_position(
        self, doc: GovernmentDocument, pos: int
    ) -> str:
        """Determine which section a text position falls in."""
        text_before = doc.full_text[:pos]
        for pattern in self.SECTION_PATTERNS:
            matches = list(pattern.finditer(text_before))
            if matches:
                last = matches[-1]
                return f"Section {last.group(1)}"
        return ""

    def parse_document(self, doc: GovernmentDocument) -> GovernmentDocument:
        """Parse a document to extract sections and citations, returning updated copy."""
        sections = self.extract_sections(doc.full_text)
        citations = self.extract_citations(doc)
        return doc.model_copy(
            update={
                "sections": sections if sections else doc.sections,
                "citations": citations if citations else doc.citations,
            }
        )
