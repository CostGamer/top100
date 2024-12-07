from typing import Any

import requests

from src.cloud_function.cloud_config import GITHUB_API_URL, HEADERS, PARAMS


class GitHubRepoFetcher:
    def __init__(
        self,
        api_url: str = GITHUB_API_URL,
        headers: dict[str, str] = HEADERS,
        params: dict[str, Any] = PARAMS,
    ):
        self.api_url = api_url
        self.headers = headers
        self.params = params

    def get_top_repos(self) -> list[dict[str, Any]]:
        try:
            response = requests.get(
                self.api_url, headers=self.headers, params=self.params
            )
            response.raise_for_status()
            return response.json().get("items", [])
        except requests.exceptions.RequestException as e:
            print(f"Error fetching repositories: {e}")
            raise
