from __future__ import annotations

from rag.chroma import VectorStore


class CertificatesTool:
    """Search Wesley's certifications and credentials."""

    name = "certificate_search"
    description = "Search Wesley's certifications, credentials, and completed courses"

    def __init__(self):
        self.store = VectorStore()

    async def execute(self, query: str) -> list[dict]:
        """Search certificate documents."""
        return self.store.search(
            query=query,
            n_results=5,
            min_score=0.3,
            filter_criteria={"category": "certificate"},
        )
