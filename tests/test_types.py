"""Tests for document types and enums."""

import pytest

from govsearch.documents.types import DocumentStatus, DocumentType, Jurisdiction


class TestDocumentType:
    def test_all_types_exist(self):
        assert DocumentType.LEGISLATION.value == "legislation"
        assert DocumentType.REGULATION.value == "regulation"
        assert DocumentType.COURT_RULING.value == "court_ruling"
        assert DocumentType.EXECUTIVE_ORDER.value == "executive_order"
        assert DocumentType.BUDGET.value == "budget"
        assert DocumentType.REPORT.value == "report"

    def test_display_name(self):
        assert DocumentType.COURT_RULING.display_name == "Court Ruling"
        assert DocumentType.EXECUTIVE_ORDER.display_name == "Executive Order"

    def test_from_string(self):
        assert DocumentType.from_string("legislation") == DocumentType.LEGISLATION
        assert DocumentType.from_string("COURT_RULING") == DocumentType.COURT_RULING
        assert DocumentType.from_string("executive order") == DocumentType.EXECUTIVE_ORDER

    def test_from_string_invalid(self):
        with pytest.raises(ValueError, match="Unknown document type"):
            DocumentType.from_string("nonexistent")


class TestJurisdiction:
    def test_jurisdictions(self):
        assert Jurisdiction.FEDERAL.value == "federal"
        assert Jurisdiction.STATE.value == "state"
        assert Jurisdiction.LOCAL.value == "local"


class TestDocumentStatus:
    def test_statuses(self):
        assert DocumentStatus.ACTIVE.value == "active"
        assert DocumentStatus.REPEALED.value == "repealed"
        assert DocumentStatus.PROPOSED.value == "proposed"
