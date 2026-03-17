"""Document indexer for building and updating search indices."""

from __future__ import annotations

from sklearn.feature_extraction.text import TfidfVectorizer

from govsearch.models import GovernmentDocument


class DocumentIndexer:
    """Indexes government documents for full-text search using TF-IDF.

    Maintains a TF-IDF matrix over all indexed documents, supporting
    incremental additions and full rebuilds.
    """

    def __init__(self) -> None:
        self._vectorizer = TfidfVectorizer(
            max_features=10000,
            stop_words="english",
            ngram_range=(1, 2),
            min_df=1,
            max_df=0.95,
            sublinear_tf=True,
        )
        self._documents: list[GovernmentDocument] = []
        self._doc_id_map: dict[str, int] = {}
        self._tfidf_matrix = None
        self._dirty = True

    @property
    def document_count(self) -> int:
        return len(self._documents)

    @property
    def tfidf_matrix(self):
        """Lazily computed TF-IDF matrix."""
        if self._dirty:
            self._rebuild_index()
        return self._tfidf_matrix

    @property
    def vectorizer(self) -> TfidfVectorizer:
        if self._dirty:
            self._rebuild_index()
        return self._vectorizer

    def add_document(self, doc: GovernmentDocument) -> None:
        """Add a single document to the index."""
        if doc.doc_id in self._doc_id_map:
            # Replace existing
            idx = self._doc_id_map[doc.doc_id]
            self._documents[idx] = doc
        else:
            self._doc_id_map[doc.doc_id] = len(self._documents)
            self._documents.append(doc)
        self._dirty = True

    def add_documents(self, docs: list[GovernmentDocument]) -> None:
        """Add multiple documents to the index."""
        for doc in docs:
            self.add_document(doc)

    def remove_document(self, doc_id: str) -> bool:
        """Remove a document from the index by ID."""
        if doc_id not in self._doc_id_map:
            return False
        idx = self._doc_id_map.pop(doc_id)
        self._documents.pop(idx)
        # Rebuild ID map
        self._doc_id_map = {d.doc_id: i for i, d in enumerate(self._documents)}
        self._dirty = True
        return True

    def get_document(self, doc_id: str) -> GovernmentDocument | None:
        """Retrieve a document by its ID."""
        idx = self._doc_id_map.get(doc_id)
        if idx is None:
            return None
        return self._documents[idx]

    def get_all_documents(self) -> list[GovernmentDocument]:
        """Return all indexed documents."""
        return list(self._documents)

    def _rebuild_index(self) -> None:
        """Rebuild the TF-IDF matrix from all documents."""
        if not self._documents:
            self._tfidf_matrix = None
            self._dirty = False
            return
        corpus = [doc.text_for_indexing for doc in self._documents]
        self._tfidf_matrix = self._vectorizer.fit_transform(corpus)
        self._dirty = False
