"""Tests for document parser."""

from datetime import date

from govsearch.documents.parser import DocumentParser
from govsearch.documents.types import DocumentType
from govsearch.models import GovernmentDocument


class TestDocumentParser:
    def setup_method(self):
        self.parser = DocumentParser()

    def test_extract_sections(self):
        text = (
            "SECTION 1. Short Title. This is the title section content.\n"
            "SECTION 2. Findings. Congress finds certain things important.\n"
            "SECTION 3. Standards. New standards are established."
        )
        sections = self.parser.extract_sections(text)
        assert len(sections) >= 2
        assert sections[0].number == "1"

    def test_extract_citations_usc(self):
        doc = GovernmentDocument(
            doc_id="P-001",
            title="Test",
            doc_type=DocumentType.LEGISLATION,
            agency="Congress",
            date_published=date(2024, 1, 1),
            full_text="Reference to 42 U.S.C. 7401 regarding air quality standards.",
        )
        citations = self.parser.extract_citations(doc)
        assert len(citations) >= 1
        assert any("U.S.C" in c.target_doc_id for c in citations)

    def test_extract_citations_cfr(self):
        doc = GovernmentDocument(
            doc_id="P-002",
            title="Test",
            doc_type=DocumentType.REGULATION,
            agency="EPA",
            date_published=date(2024, 1, 1),
            full_text="Per 40 C.F.R. Part 50 requirements for air quality.",
        )
        citations = self.parser.extract_citations(doc)
        assert len(citations) >= 1

    def test_extract_dates(self):
        text = "Effective January 15, 2024 and amended on 2024-06-01."
        dates = self.parser.extract_dates(text)
        assert len(dates) >= 2
        assert date(2024, 1, 15) in dates
        assert date(2024, 6, 1) in dates

    def test_extract_dates_us_format(self):
        dates = self.parser.extract_dates("Filed on 3/15/2024.")
        assert date(2024, 3, 15) in dates

    def test_parse_document(self):
        doc = GovernmentDocument(
            doc_id="P-003",
            title="Parsed Doc",
            doc_type=DocumentType.LEGISLATION,
            agency="Congress",
            date_published=date(2024, 1, 1),
            full_text=(
                "SECTION 1. Title. Short title section.\n"
                "SECTION 2. References. See 42 U.S.C. 7401.\n"
                "SECTION 3. Conclusion. Final provisions."
            ),
        )
        parsed = self.parser.parse_document(doc)
        assert len(parsed.sections) >= 2
        assert len(parsed.citations) >= 1

    def test_fallback_paragraph_sections(self):
        text = "First paragraph with some content.\n\nSecond paragraph here.\n\nThird paragraph."
        sections = self.parser.extract_sections(text)
        assert len(sections) >= 2
