import asyncio
from typing import Any

import aiohttp

from src.cloud_function.cloud_config import (
    GITHUB_API_URL,
    HEADERS,
    REPO_PARAMS,
)


class GitHubFetcher:
    def __init__(
        self,
        api_url: str = GITHUB_API_URL,
        headers: dict[str, str] = HEADERS,
        repo_params: dict[str, Any] = REPO_PARAMS,
    ):
        self.api_url = api_url
        self.headers = headers
        self.repo_params = repo_params

    async def get_top_repos(self) -> list[dict[str, Any]]:
        try:
            async with aiohttp.ClientSession(headers=self.headers) as session:
                async with session.get(
                    self.api_url, params=self.repo_params
                ) as response:
                    response.raise_for_status()
                    data = await response.json()
                    return data.get("items", [])
        except aiohttp.ClientError as e:
            print(f"Error fetching repositories: {e}")
            raise

    async def get_commits(self, owner: str, repo: str) -> list[dict[str, Any]]:
        commits = []
        page = 1
        semaphore = asyncio.Semaphore(
            5
        )  # Ограничиваем количество параллельных запросов

        async def fetch_page(page):
            params = {"page": page, "per_page": 100}
            url = f"https://api.github.com/repos/{owner}/{repo}/commits"

            async with semaphore, aiohttp.ClientSession() as session:
                async with session.get(
                    url, headers=self.headers, params=params
                ) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        raise aiohttp.ClientResponseError(
                            response.request_info,
                            response.history,
                            code=response.status,
                        )

        try:
            while True:
                data = await fetch_page(page)
                if not data:
                    break
                commits.extend(data)
                page += 1
        except Exception as e:
            print(f"Error fetching commits: {e}")
            raise

        return commits
