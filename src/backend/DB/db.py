from contextlib import asynccontextmanager
from typing import AsyncGenerator

import psycopg
from psycopg_pool import AsyncConnectionPool

from src.backend.DB.settings import all_settings
from src.backend.logs import setup_logger

logger = setup_logger(__name__)


class DatabasePool:
    def __init__(self) -> None:
        self._pool: AsyncConnectionPool | None = None

    async def init_async_pool(self) -> None:
        if self._pool is None:
            self._pool = AsyncConnectionPool(
                conninfo=all_settings.db_uri,
                min_size=1,
                max_size=10,
            )
            logger.info("Connection pool initialized")

    async def close_async_pool(self) -> None:
        if self._pool is not None:
            await self._pool.close()
            self._pool = None
            logger.info("Connection pool closed")

    @asynccontextmanager
    async def get_connection(self) -> AsyncGenerator[psycopg.AsyncConnection, None]:
        if self._pool is None:
            raise RuntimeError("Connection pool is not initialized.")
        async with self._pool.connection() as conn:
            try:
                yield conn
                await conn.commit()
            except Exception as e:
                await conn.rollback()
                logger.warning(f"Error: {e}")
                raise


database_pool = DatabasePool()


async def get_db() -> AsyncGenerator[psycopg.AsyncConnection, None]:
    async with database_pool.get_connection() as conn:
        yield conn
