from __future__ import annotations

import logging
import os

import chromadb
from chromadb.config import Settings

from rag.embeddings import EmbeddingService

logger = logging.getLogger(__name__)


class VectorStore:
    """ChromaDB vector store for RAG retrieval.

    Uses ChromaDB in embedded mode — no external server needed.
    The index is pre-built during Docker image build and loaded at startup.
    """

    _instance: VectorStore | None = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(
        self,
        persist_dir: str = "index",
        collection_name: str = "portfolio",
    ):
        if hasattr(self, "_initialized") and self._initialized:
            return

        self.persist_dir = persist_dir
        self.collection_name = collection_name
        self.embeddings = EmbeddingService()
        self._client: chromadb.Client | None = None
        self._collection: chromadb.Collection | None = None
        self._initialized = True

    @property
    def client(self) -> chromadb.Client:
        if self._client is None:
            os.makedirs(self.persist_dir, exist_ok=True)
            self._client = chromadb.PersistentClient(
                path=self.persist_dir,
                settings=Settings(anonymized_telemetry=False),
            )
            logger.info("ChromaDB client initialized at %s", self.persist_dir)
        return self._client

    @property
    def collection(self) -> chromadb.Collection:
        if self._collection is None:
            try:
                self._collection = self.client.get_collection(self.collection_name)
                count = self._collection.count()
                logger.info("Loaded collection '%s' with %d documents", self.collection_name, count)
            except ValueError:
                logger.warning("Collection '%s' not found. Creating empty collection.", self.collection_name)
                self._collection = self.client.create_collection(
                    name=self.collection_name,
                    metadata={"hnsw:space": "cosine"},
                )
        return self._collection

    def add_documents(
        self,
        documents: list[str],
        metadatas: list[dict],
        ids: list[str],
    ) -> None:
        """Add documents to the vector store."""
        self.collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids,
        )
        logger.info("Added %d documents to collection", len(documents))

    def search(
        self,
        query: str,
        n_results: int = 5,
        min_score: float = 0.5,
        filter_criteria: dict | None = None,
    ) -> list[dict]:
        """Search for similar documents.

        Args:
            query: The search query.
            n_results: Maximum number of results to return.
            min_score: Minimum similarity score threshold (0-1).
            filter_criteria: Optional metadata filters.

        Returns:
            List of dicts with 'content', 'metadata', and 'score' keys.
        """
        if self.collection.count() == 0:
            return []

        results = self.collection.query(
            query_texts=[query],
            n_results=n_results,
            where=filter_criteria,
        )

        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]
        distances = results.get("distances", [[]])[0]

        # Chroma returns distances (0 = identical, 2 = opposite)
        # Convert to similarity score (1 - distance/2)
        filtered = []
        for doc, meta, dist in zip(documents, metadatas, distances):
            score = 1.0 - (dist / 2.0)
            if score >= min_score:
                filtered.append({
                    "content": doc,
                    "metadata": meta,
                    "score": round(score, 3),
                })

        return filtered

    def get_document_count(self) -> int:
        """Return total document count in the collection."""
        try:
            return self.collection.count()
        except ValueError:
            return 0

    def is_loaded(self) -> bool:
        """Check if the collection has data."""
        return self.get_document_count() > 0

    def delete_collection(self) -> None:
        """Delete and recreate the collection."""
        try:
            self.client.delete_collection(self.collection_name)
        except ValueError:
            pass
        self._collection = None
        logger.info("Collection deleted")
