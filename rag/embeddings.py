from __future__ import annotations

import logging

from fastembed import TextEmbedding

logger = logging.getLogger(__name__)


class EmbeddingService:
    """Wrapper around FastEmbed for generating text embeddings.

    Uses BAAI/bge-small-en-v1.5 — a lightweight, fast model that runs
    in-process without GPU or heavy dependencies.
    """

    _instance: EmbeddingService | None = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, model_name: str = "BAAI/bge-small-en-v1.5"):
        if hasattr(self, "_initialized") and self._initialized:
            return
        self.model_name = model_name
        self._model: TextEmbedding | None = None
        self._initialized = True

    @property
    def model(self) -> TextEmbedding:
        if self._model is None:
            logger.info("Loading embedding model: %s", self.model_name)
            self._model = TextEmbedding(model_name=self.model_name, max_length=512)
            logger.info("Embedding model loaded")
        return self._model

    def embed(self, text: str) -> list[float]:
        """Generate embedding vector for a single text string."""
        return list(self.embed_batch([text])[0])

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """Generate embedding vectors for a batch of texts."""
        embeddings = list(self.model.embed(texts))
        return [list(e) for e in embeddings]

    @property
    def dimension(self) -> int:
        """Return the embedding dimension."""
        # BGE-small-en-v1.5 produces 384-dimensional vectors
        return 384
