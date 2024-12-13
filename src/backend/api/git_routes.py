from fastapi import APIRouter, Depends, Query
from psycopg import AsyncConnection

from src.backend.api.exceptions import (
    incorrect_date_format,
    owner_does_not_exist,
    param_not_valid,
    params_incorrect_format,
    repo_does_not_exist,
    until_is_bigger_than_since,
    with_errors,
)
from src.backend.app.gateways.commit_qateway import CommitGateway
from src.backend.app.gateways.repo_qateway import RepoGateway
from src.backend.app.interactions.commit_interactor import GetCommitInteractor
from src.backend.app.interactions.custom_exceptions import (
    DateFormatIsIncorrect,
    FormatIsIncorrect,
    OwnerDoesNotExist,
    ParamIsIncorrect,
    RepoDoesNotExist,
    UntilIsBiggerThanSince,
)
from src.backend.app.interactions.repo_interactor import GetRepoInteractor
from src.backend.app.pydantic_tabels import activity, top_100
from src.backend.DB.db import get_db

git_router = APIRouter()


@git_router.get(
    "/top100",
    response_model=list[top_100],
    responses=with_errors(
        params_incorrect_format,
        param_not_valid,
    ),
    description="Endpoint that fetch top 100 GIT repositories by stars. Also you can send sorted parameter(es)",
)
async def get_top_100_repo(
    sort_params: str | None = Query(None, example="repo, owner"),
    db: AsyncConnection = Depends(get_db),
) -> list[top_100]:
    top_100_gateway = RepoGateway(db)
    top_100_interactor = GetRepoInteractor(top_100_gateway)

    try:
        return await top_100_interactor(sort_params)
    except RuntimeError:
        raise
    except FormatIsIncorrect:
        raise params_incorrect_format
    except ParamIsIncorrect:
        raise param_not_valid


@git_router.get(
    "/{owner}/{repo}/activity",
    response_model=list[activity],
    responses=with_errors(
        owner_does_not_exist,
        repo_does_not_exist,
        until_is_bigger_than_since,
        incorrect_date_format,
    ),
    description="Endpoint that fetches repository activity for a specified period",
)
async def get_repo_activity(
    owner: str,
    repo: str,
    since: str = Query(example="2025-01-20"),
    until: str = Query(example="2025-01-20"),
    db: AsyncConnection = Depends(get_db),
) -> list[activity]:
    commit_gateway = CommitGateway(db)
    commit_interactor = GetCommitInteractor(commit_gateway)

    try:
        return await commit_interactor(owner, repo, since, until)
    except OwnerDoesNotExist:
        raise owner_does_not_exist
    except RepoDoesNotExist:
        raise repo_does_not_exist
    except UntilIsBiggerThanSince:
        raise until_is_bigger_than_since
    except DateFormatIsIncorrect:
        raise incorrect_date_format
    except RuntimeError:
        raise
