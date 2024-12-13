from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.backend.api.git_routes import git_router
from src.backend.DB.db import close_async_pool, init_async_pool
from src.backend.logs import setup_logger


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
    await init_async_pool()
    yield
    await close_async_pool()


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
    return app
