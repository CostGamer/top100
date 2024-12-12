from psycopg import AsyncConnection
from psycopg.rows import dict_row


class RepoGateway:
    def __init__(self, con: AsyncConnection) -> None:
        self._con = con

    async def get_top_100_repo_sorted(self, sort_params: str) -> list[dict]:
        query = """
            SELECT *
            FROM top100
            ORDER BY %(sort_field)s
            LIMIT 100;
            """
        async with self._con.cursor(row_factory=dict_row) as cursor:
            await cursor.execute(query, params={"sort_field": sort_params})
            return await cursor.fetchall()
