import psycopg
from psycopg import AsyncConnection

from src.cloud_function.cloud_config import DB_URI


async def get_db_connection() -> AsyncConnection:
    try:
        # self.connection = psycopg.connect(
        #     host=DB_HOST,
        #     port=DB_PORT,
        #     user=DB_USER,
        #     password=DB_PASSWORD,
        #     database=DB_NAME
        # )
        async_connection = await psycopg.AsyncConnection.connect(DB_URI)
        return async_connection
    except Exception as e:
        print(f"DB connection errro: {e}")
        raise


async def execute_query(query: str, params: tuple | None = None) -> list[tuple] | None:  # type: ignore
    async with await get_db_connection() as async_connection:
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
