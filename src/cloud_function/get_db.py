from psycopg_pool import AsyncConnectionPool

from src.cloud_function.cloud_config import DB_URI


async def init_async_pool() -> AsyncConnectionPool:
    pool = AsyncConnectionPool(
        conninfo=DB_URI,
        min_size=1,
        max_size=10,
    )
    return pool


async def get_db_and_execute(
    query: str,
    params: dict | None = None,
    pool: AsyncConnectionPool | None = None,
) -> list[tuple] | None:  # type: ignore
    if pool is None:
        raise RuntimeError("Connection pool is not initialized.")
    async with pool.connection() as async_connection:
        async with async_connection.cursor() as cursor:
            try:
                await cursor.execute(query, params)
                if query.strip().upper().startswith("SELECT"):
                    return await cursor.fetchall()
                else:
                    await async_connection.commit()
            except Exception as e:
                print(f"Query error: {e}")
                await async_connection.rollback()
                raise
