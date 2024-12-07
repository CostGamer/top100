from typing import Any


class GitHubRepoParser:
    def parse_repo_data(self, repos: list[dict[str, Any]]) -> list[dict[str, Any]]:
        parsed_data = []
        for position_cur, repo in enumerate(repos, start=1):
            parsed_repo = {
                "repo": repo["full_name"],
                "owner": repo["owner"]["login"],
                "position_cur": position_cur,
                "position_prev": None,
                "stars": repo["stargazers_count"],
                "watchers": repo["watchers_count"],
                "forks": repo["forks_count"],
                "open_issues": repo["open_issues_count"],
                "language": repo["language"],
            }
            parsed_data.append(parsed_repo)
        return parsed_data
