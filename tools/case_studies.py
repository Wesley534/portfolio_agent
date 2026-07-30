from __future__ import annotations

from rag.chroma import VectorStore


class CaseStudiesTool:
    """Search Wesley's engineering case studies."""

    name = "case_study_search"
    description = "Search case studies of Wesley's engineering projects and infrastructure work"

    def __init__(self):
        self.store = VectorStore()

    async def execute(self, query: str) -> list[dict]:
        """Search case study documents."""
        return self.store.search(
            query=query,
            n_results=5,
            min_score=0.3,
            filter_criteria={"category": "case_study"},
        )
