from fastapi import APIRouter, Depends, Query

from src.backend.api.responses import (
    get_repo_activity_responses,
    get_top_100_repo_responses,
)
from src.backend.app.interactions.commit_interactor import GetCommitInteractor
from src.backend.app.interactions.repo_interactor import GetRepoInteractor
from src.backend.app.pydantic_tabels import Activity, Top100
from src.backend.app.repo import get_commit_interactor, get_repo_interactor

git_router = APIRouter()


@git_router.get(
    "/top100",
    response_model=list[Top100],
    responses=get_top_100_repo_responses,
    description="Endpoint that fetch top 100 GIT repositories by stars. Also you can send sorted parameter(es)",
)
async def get_top_100_repo(
    sort_params: str | None = Query(None, example="repo, owner"),
    top_100_interactor: GetRepoInteractor = Depends(get_repo_interactor),
) -> list[Top100]:
    return await top_100_interactor(sort_params)


@git_router.get(
    "/{owner}/{repo}/activity",
    response_model=list[Activity],
    responses=get_repo_activity_responses,
    description="Endpoint that fetches repository activity for a specified period",
)
async def get_repo_activity(
    owner: str,
    repo: str,
    since: str = Query(example="2025-01-20"),
    until: str = Query(example="2025-01-20"),
    commit_interactor: GetCommitInteractor = Depends(get_commit_interactor),
) -> list[Activity]:
    return await commit_interactor(owner, repo, since, until)
