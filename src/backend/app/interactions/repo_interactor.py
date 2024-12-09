from src.backend.app.gateways.repo_qateway import RepoGateway
from src.backend.app.interactions.custom_exceptions import (
    FormatIsIncorrect,
    ParamIsIncorrect,
)
from src.backend.app.pydantic_tabels import top_100
from src.backend.DB.settings import VALID_PARAMS


class GetRepoInteractor:
    def __init__(self, repo_gateway: RepoGateway) -> None:
        self._repo_gateway = repo_gateway

    async def __call__(self, sort_params: str | None = None) -> list[top_100]:
        sort_clause = await self._process_sort_params(sort_params)
        try:
            top_100_repo = await self._repo_gateway.get_top_100_repo_sorted(sort_clause)
            return [top_100.model_validate(repo) for repo in top_100_repo]
        except Exception as e:
            raise RuntimeError(f"Error: {e}")

    async def _process_sort_params(self, sort_params: str | None) -> str:
        if not sort_params:
            return "position_cur"

        try:
            sort_params_list = [param.strip() for param in sort_params.split(",")]
        except Exception:
            raise FormatIsIncorrect

        if not all(param in VALID_PARAMS for param in sort_params_list):
            raise ParamIsIncorrect

        if len(sort_params_list) > 1:
            return ", ".join(sort_params_list)
        return sort_params_list[0]
