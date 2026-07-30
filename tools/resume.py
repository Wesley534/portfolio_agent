from __future__ import annotations

from rag.chroma import VectorStore


class ResumeTool:
    """Search Wesley's resume and professional background."""

    name = "resume_search"
    description = "Search Wesley's resume, experience, education, and professional background"

    def __init__(self):
        self.store = VectorStore()

    async def execute(self, query: str) -> list[dict]:
        """Search resume documents."""
        return self.store.search(
            query=query,
            n_results=5,
            min_score=0.3,
            filter_criteria={"category": "resume"},
        )
