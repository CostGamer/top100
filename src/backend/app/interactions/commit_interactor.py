from datetime import date as set_date
from datetime import datetime, timedelta, timezone

import aiohttp

from src.backend.app.gateways.commit_qateway import CommitGateway
from src.backend.app.interactions.custom_exceptions import (
    DateFormatIsIncorrect,
    OwnerDoesNotExist,
    RepoDoesNotExist,
    UntilIsBiggerThanSince,
)
from src.backend.app.pydantic_tabels import activity
from src.backend.DB.settings import all_settings


class GetCommitInteractor:
    def __init__(self, commit_gateway: CommitGateway) -> None:
        self._commit_gateway = commit_gateway

    async def __call__(
        self,
        owner: str,
        repo: str,
        since: str,
        until: str,
    ) -> list[activity]:
        commits_list = []

        if not await self._commit_gateway.check_owner_exists(owner):
            raise OwnerDoesNotExist

        if not await self._commit_gateway.check_repo_exists(repo):
            raise RepoDoesNotExist

        new_since = self._check_change_date_format(since)
        new_until = self._check_change_date_format(until)

        if not self._check_until_more_than_since(new_since, new_until):
            raise UntilIsBiggerThanSince

        exact_day = new_since
        today = datetime.now(timezone.utc).date()
        while exact_day <= new_until:
            try:
                day_activity = await self._commit_gateway.get_commit_activity_per_day(
                    owner, repo, exact_day
                )

                if exact_day == today and day_activity is not None:
                    await self._fetch_and_update_commits(owner, repo, exact_day)

                if day_activity is None:
                    commits_data = await self._fetch_and_store_commits(
                        owner, repo, exact_day
                    )
                    commits_list.append(commits_data)
                else:
                    commits_list.append(day_activity)
            except Exception as e:
                raise RuntimeError(
                    f"Unexpected error during processing for {exact_day}: {e}"
                )

            exact_day += timedelta(days=1)

        return [activity.model_validate(commmit) for commmit in commits_list]

    async def _fetch_and_store_commits(
        self, owner: str, repo: str, date: set_date
    ) -> dict:
        fetch_res = await self._fetch_commits_activity_from_net(
            repo, owner, date.strftime("%Y-%m-%d")
        )
        await self._commit_gateway.push_data_for_exact_date_to_db(
            owner, repo, date, fetch_res[0], fetch_res[1]
        )
        return {"date": date, "commits": fetch_res[0], "authors": fetch_res[1]}

    async def _fetch_and_update_commits(
        self, repo: str, owner: str, date: set_date
    ) -> dict:
        fetch_res = await self._fetch_commits_activity_from_net(
            repo, owner, date.strftime("%Y-%m-%d")
        )
        await self._commit_gateway.update_commits_data_today(
            owner, repo, date, fetch_res[0], fetch_res[1]
        )
        return {"date": date, "commits": fetch_res[0], "authors": fetch_res[1]}

    @staticmethod
    def _check_until_more_than_since(since: set_date, until: set_date) -> bool:
        return since <= until

    @staticmethod
    def _check_change_date_format(check_date: str) -> datetime:
        try:
            return datetime.strptime(check_date, "%Y-%m-%d")
        except ValueError:
            raise DateFormatIsIncorrect

    @staticmethod
    async def _fetch_commits_activity_from_net(
        repo: str, owner: str, date: str
    ) -> tuple[int, list[str]]:
        authors: set[str] = set()
        total_commits = 0
        page = 1
        per_page = 100

        async with aiohttp.ClientSession(headers=all_settings.headers) as session:
            while True:
                url = f"{all_settings.github_api_url}/{owner}/{repo}/commits"
                params = {
                    "since": f"{date}T00:00:00Z",
                    "until": f"{date}T23:59:59Z",
                    "per_page": str(per_page),
                    "page": str(page),
                }

                async with session.get(url, params=params) as response:
                    if response.status != 200:
                        print(
                            f"Error fetching commits: {response.status}, {response.text}"
                        )
                        return total_commits, list(authors)

                    data = await response.json()

                    if not data:
                        print("No commits found for this date.")
                        break

                    for commit in data:
                        total_commits += 1
                        authors.add(commit["commit"]["author"]["name"])

                    if len(data) < per_page:
                        break

                    page += 1

        return total_commits, list(authors)
