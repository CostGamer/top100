from typing import Any

import aiohttp
from tenacity import retry, stop_after_attempt, wait_fixed

from src.cloud_function.cloud_config import (
    # GITHUB_API_URL_COMMITS,
    GITHUB_API_URL_REPO,
    HEADERS,
    REPO_PARAMS,
)


class GitHubFetcher:
    def __init__(
        self,
        api_url_repo: str = GITHUB_API_URL_REPO,
        # api_url_commit: str = GITHUB_API_URL_COMMITS,
        headers: dict[str, str] = HEADERS,
        repo_params: dict[str, Any] = REPO_PARAMS,
    ):
        self.api_url_repo = api_url_repo
        # self.api_url_commit = api_url_commit
        self.headers = headers
        self.repo_params = repo_params

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    async def get_top_repos(self) -> list[dict[str, Any]]:
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.get(
                self.api_url_repo, params=self.repo_params
            ) as response:
                response.raise_for_status()
                data = await response.json()
                return data.get("items", [])

    # @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    # async def get_activity(self, owner: str, repo: str) -> list[dict[str, Any]]:
    #     activity_url = f"{self.api_url_commit}/repos/{owner}/{repo}/commits"
    #     async with aiohttp.ClientSession(headers=self.headers) as session:
    #         async with session.get(activity_url) as response:
    #             response.raise_for_status()
    #             data = await response.json()
    #             return data
