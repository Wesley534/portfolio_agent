from __future__ import annotations

import logging
import os

import httpx

logger = logging.getLogger(__name__)

TRUSTED_DOMAINS = [
    "github.com",
    "github.com/Wesley534",
    "linkedin.com/in/peter-wesley",
    "docs.python.org",
    "fastapi.tiangolo.com",
]


class WebSearchTool:
    """Search the web — restricted to trusted domains only.

    Uses Tavily API if configured, otherwise returns a message about restricted search.
    """

    name = "web_search"
    description = "Search the web (restricted to trusted domains like GitHub, documentation)"

    async def execute(self, query: str) -> dict:
        """Perform a restricted web search."""
        tavily_key = os.getenv("TAVILY_API_KEY")

        if tavily_key:
            return await self._tavily_search(query, tavily_key)

        # No API key — return domain suggestions
        return {
            "results": [
                {
                    "title": "Web search not configured",
                    "url": "",
                    "content": (
                        "I can search trusted sources like GitHub and LinkedIn for you. "
                        "What specifically are you looking for?"
                    ),
                }
            ],
            "note": "Web search uses Tavily API. Configure TAVILY_API_KEY for full functionality.",
        }

    async def _tavily_search(self, query: str, api_key: str) -> dict:
        """Search using Tavily API with domain restrictions."""
        domain_filter = " OR ".join(f"site:{d}" for d in TRUSTED_DOMAINS)
        full_query = f"{query} ({domain_filter})"

        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                response = await client.post(
                    "https://api.tavily.com/search",
                    json={
                        "api_key": api_key,
                        "query": full_query,
                        "search_depth": "basic",
                        "max_results": 5,
                        "include_domains": TRUSTED_DOMAINS,
                    },
                )
                response.raise_for_status()
                data = response.json()
                return {
                    "results": [
                        {
                            "title": r.get("title", ""),
                            "url": r.get("url", ""),
                            "content": r.get("content", ""),
                        }
                        for r in data.get("results", [])
                    ]
                }
            except Exception as e:
                logger.error("Tavily search failed: %s", e)
                return {"results": [], "error": str(e)}
