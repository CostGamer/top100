from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.backend.api.exceptions import (
    incorrect_date_format,
    owner_does_not_exist,
    param_not_valid,
    params_incorrect_format,
    repo_does_not_exist,
    runtime_error_exception_handler,
    until_is_bigger_than_since,
)
from src.backend.api.git_routes import git_router
from src.backend.app.interactions.custom_exceptions import (
    DateFormatIsIncorrect,
    FormatIsIncorrect,
    OwnerDoesNotExist,
    ParamIsIncorrect,
    RepoDoesNotExist,
    UntilIsBiggerThanSince,
)
from src.backend.DB.db import database_pool
from src.backend.logs import setup_logger


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(FormatIsIncorrect, params_incorrect_format)  # type: ignore
    app.add_exception_handler(ParamIsIncorrect, param_not_valid)  # type: ignore
    app.add_exception_handler(OwnerDoesNotExist, owner_does_not_exist)  # type: ignore
    app.add_exception_handler(RepoDoesNotExist, repo_does_not_exist)  # type: ignore
    app.add_exception_handler(UntilIsBiggerThanSince, until_is_bigger_than_since)  # type: ignore
    app.add_exception_handler(DateFormatIsIncorrect, incorrect_date_format)  # type: ignore
    app.add_exception_handler(RuntimeError, runtime_error_exception_handler)  # type: ignore


def init_routers(app: FastAPI) -> None:
    app.include_router(git_router, prefix="/api/repos", tags=["git"])


def init_middlewares(app: FastAPI) -> None:
    origins = [
        "http://localhost:8000",
        "http://127.0.0.1:8000",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[Any, Any]:
    await database_pool.init_async_pool()
    yield
    await database_pool.close_async_pool()


def setup_app() -> FastAPI:
    app = FastAPI(
        title="top100",
        description="API for top100 GIT",
        version="0.0.1",
        lifespan=lifespan,
    )
    setup_logger("top100")
    init_routers(app)
    init_middlewares(app)
    register_exception_handlers(app)
    return app
