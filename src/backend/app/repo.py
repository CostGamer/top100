from fastapi import Depends
from psycopg import AsyncConnection

from src.backend.app.gateways.commit_qateway import CommitGateway
from src.backend.app.gateways.repo_qateway import RepoGateway
from src.backend.app.interactions.commit_interactor import GetCommitInteractor
from src.backend.app.interactions.repo_interactor import GetRepoInteractor
from src.backend.DB.db import get_db


def get_repo_gateway(db: AsyncConnection = Depends(get_db)) -> RepoGateway:
    return RepoGateway(db)


def get_commit_gateway(db: AsyncConnection = Depends(get_db)) -> CommitGateway:
    return CommitGateway(db)


def get_repo_interactor(
    repo_gateway: RepoGateway = Depends(get_repo_gateway),
) -> GetRepoInteractor:
    return GetRepoInteractor(repo_gateway)


def get_commit_interactor(
    commit_gateway: CommitGateway = Depends(get_commit_gateway),
) -> GetCommitInteractor:
    return GetCommitInteractor(commit_gateway)
