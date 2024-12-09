from datetime import date as set_date
from datetime import datetime

from src.backend.app.gateways.commit_qateway import CommitGateway
from src.backend.app.interactions.custom_exceptions import (
    DateFormatIsIncorrect,
    OwnerDoesNotExist,
    RepoDoesNotExist,
    UntilIsBiggerThanSince,
)
from src.backend.app.pydantic_tabels import activity


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
        check_owner_exists = await self._commit_gateway.check_owner_exists(owner)
        if not check_owner_exists:
            raise OwnerDoesNotExist

        check_repo_exists = await self._commit_gateway.check_repo_exists(repo)
        if not check_repo_exists:
            raise RepoDoesNotExist

        new_since = self._check_change_date_format(since)
        new_until = self._check_change_date_format(until)

        check_date_logic_correctness = self._check_until_more_than_since(
            new_since, new_until
        )
        if not check_date_logic_correctness:
            raise UntilIsBiggerThanSince

        try:
            commit_list = await self._commit_gateway.get_commit_activity(
                owner, repo, new_since, new_until
            )
            return [activity.model_validate(commit) for commit in commit_list]
        except Exception as e:
            raise RuntimeError(f"Unexpected error: {e}")

    @staticmethod
    def _check_until_more_than_since(since: set_date, until: set_date) -> bool:
        return since <= until

    @staticmethod
    def _check_change_date_format(check_date: str) -> datetime:
        try:
            return datetime.strptime(check_date, "%Y-%m-%d")
        except ValueError:
            raise DateFormatIsIncorrect
