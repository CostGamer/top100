from functools import lru_cache
from typing import AsyncGenerator

import psycopg
from psycopg_pool import AsyncConnectionPool

from src.backend.DB.settings import all_settings


@lru_cache()
async def get_async_pool() -> AsyncConnectionPool:
    return AsyncConnectionPool(conninfo=all_settings.db_uri)


async def get_db(pool: AsyncConnectionPool) -> AsyncGenerator[psycopg.AsyncConnection, None]:
    async with pool.connection() as conn:
        try:
            yield conn
            await conn.commit()
        except Exception as e:
            await conn.rollback()
            print(f"Error: {e}")
            raise
