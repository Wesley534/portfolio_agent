from __future__ import annotations

import logging
import os

import httpx

logger = logging.getLogger(__name__)


class GitHubTool:
    """Search Wesley's GitHub repositories and README files."""

    name = "github_search"
    description = "Search Wesley's GitHub repositories and open-source projects"

    GITHUB_USERNAME = "Wesley534"

    async def execute(self, query: str = "") -> list[dict]:
        """Search GitHub repositories for the user."""
        token = os.getenv("GITHUB_TOKEN", "")
        headers = {"Accept": "application/vnd.github.v3+json"}
        if token:
            headers["Authorization"] = f"Bearer {token}"

        async with httpx.AsyncClient(headers=headers, timeout=10.0) as client:
            try:
                # Fetch all repos
                repos_response = await client.get(
                    f"https://api.github.com/users/{self.GITHUB_USERNAME}/repos",
                    params={"per_page": 30, "sort": "updated", "direction": "desc"},
                )
                repos_response.raise_for_status()
                repos = repos_response.json()

                results = []
                for repo in repos:
                    # Simple local search
                    if not query or any(
                        word.lower() in (repo.get("name", "") + repo.get("description", "")).lower()
                        for word in query.split()
                    ):
                        results.append({
                            "name": repo["name"],
                            "description": repo.get("description") or "No description",
                            "url": repo["html_url"],
                            "language": repo.get("language"),
                            "stars": repo.get("stargazers_count", 0),
                            "topics": repo.get("topics", []),
                        })

                return results[:10]  # Limit to 10 results

            except Exception as e:
                logger.error("GitHub API request failed: %s", e)
                return []
