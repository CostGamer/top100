from psycopg import AsyncConnection


class RepoGateway:
    def __init__(self, con: AsyncConnection) -> None:
        self._con = con

    async def get_top_100_repo_sorted(self, sort_params: str) -> list[tuple]:
        query = """
        SELECT *
        FROM top100
        ORDER BY %s
        LIMIT 100;
        """
        async with self._con.cursor() as cursor:
            await cursor.execute(query, params=sort_params)
            return await cursor.fetchall()
