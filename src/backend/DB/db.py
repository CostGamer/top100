from typing import AsyncGenerator

import psycopg
from psycopg_pool import AsyncConnectionPool

from src.backend.DB.settings import all_settings
from src.backend.logs import setup_logger

_pool: AsyncConnectionPool | None = None
logger = setup_logger(__name__)


async def init_async_pool() -> None:
    global _pool
    if _pool is None:
        _pool = AsyncConnectionPool(conninfo=all_settings.db_uri)
        logger.info("Connection pool initialized")


async def close_async_pool() -> None:
    global _pool
    if _pool is not None:
        await _pool.close()
        _pool = None
        logger.info("Connection pool closed")


# @asynccontextmanager
async def get_db() -> AsyncGenerator[psycopg.AsyncConnection, None]:
    global _pool
    if _pool is None:
        raise RuntimeError("Connection pool is not initialized.")
    async with _pool.connection() as conn:
        try:
            yield conn
            await conn.commit()
        except Exception as e:
            await conn.rollback()
            logger.warning(f"Error: {e}")
            raise


# async def execute_query(query: str, params: tuple = ()) -> list[tuple]:
#     async with get_db() as conn:
#         async with conn.cursor() as cursor:
#             try:
#                 await cursor.execute(query, params)
#                 if query.strip().upper().startswith("SELECT"):
#                     return await cursor.fetchall()
#                 else:
#                     return []
#             except Exception as e:
#                 logger.warning(f"Error executing query: {e}")
#                 raise
