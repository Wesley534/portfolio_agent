from __future__ import annotations

from rag.chroma import VectorStore


class BlogTool:
    """Search Wesley's blog posts and articles."""

    name = "blog_search"
    description = "Search Wesley's blog posts, articles, and technical writing"

    def __init__(self):
        self.store = VectorStore()

    async def execute(self, query: str) -> list[dict]:
        """Search blog documents."""
        return self.store.search(
            query=query,
            n_results=5,
            min_score=0.3,
            filter_criteria={"category": "blog"},
        )
