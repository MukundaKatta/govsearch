"""Tests for the document database."""

from datetime import date

from govsearch.documents.database import DocumentDatabase
from govsearch.documents.types import DocumentType, Jurisdiction
from govsearch.models import GovernmentDocument


class TestDocumentDatabase:
    def test_loads_sample_documents(self):
        db = DocumentDatabase(load_samples=True)
        assert db.count() >= 50

    def test_empty_database(self):
        db = DocumentDatabase(load_samples=False)
        assert db.count() == 0

    def test_add_and_get(self):
        db = DocumentDatabase(load_samples=False)
        doc = GovernmentDocument(
            doc_id="T-001",
            title="Test",
            doc_type=DocumentType.REPORT,
            agency="Test Agency",
            date_published=date(2024, 1, 1),
            full_text="Content.",
        )
        db.add(doc)
        assert db.count() == 1
        assert db.get("T-001") is not None
        assert db.get("T-001").title == "Test"

    def test_get_nonexistent(self):
        db = DocumentDatabase(load_samples=False)
        assert db.get("NOPE") is None

    def test_remove(self):
        db = DocumentDatabase(load_samples=False)
        doc = GovernmentDocument(
            doc_id="T-002",
            title="To Remove",
            doc_type=DocumentType.BUDGET,
            agency="A",
            date_published=date(2024, 1, 1),
            full_text="x",
        )
        db.add(doc)
        assert db.remove("T-002") is True
        assert db.count() == 0
        assert db.remove("T-002") is False

    def test_get_by_type(self):
        db = DocumentDatabase(load_samples=True)
        legislation = db.get_by_type(DocumentType.LEGISLATION)
        assert len(legislation) >= 10
        assert all(d.doc_type == DocumentType.LEGISLATION for d in legislation)

    def test_get_by_agency(self):
        db = DocumentDatabase(load_samples=True)
        epa_docs = db.get_by_agency("EPA")
        assert len(epa_docs) >= 1

    def test_search_title(self):
        db = DocumentDatabase(load_samples=True)
        results = db.search_title("Clean Air")
        assert len(results) >= 1
        assert any("Clean Air" in d.title for d in results)

    def test_all_documents(self):
        db = DocumentDatabase(load_samples=True)
        all_docs = db.all_documents()
        assert len(all_docs) == db.count()
