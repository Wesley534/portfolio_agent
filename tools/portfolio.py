from __future__ import annotations

from rag.chroma import VectorStore


class PortfolioTool:
    """Search Wesley's projects and portfolio work."""

    name = "portfolio_search"
    description = "Search through Wesley's projects, portfolio, and technical work"

    def __init__(self):
        self.store = VectorStore()

    async def execute(self, query: str) -> list[dict]:
        """Search portfolio for projects matching the query."""
        return self.store.search(
            query=query,
            n_results=5,
            min_score=0.3,
            filter_criteria={"category": "project"},
        )
