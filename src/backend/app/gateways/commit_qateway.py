from datetime import date as set_date

from psycopg import AsyncConnection
from psycopg.rows import dict_row


class CommitGateway:
    def __init__(self, con: AsyncConnection) -> None:
        self._con = con

    async def get_commit_activity(
        self,
        owner: str,
        repo: str,
        since: set_date,
        until: set_date,
    ) -> list[dict]:
        query = """
            SELECT date, commits, authors
            FROM activity
            WHERE owner = %(owner)s
            AND repo = %(repo)s
            AND date BETWEEN %(since)s AND %(until)s;
            """
        async with self._con.cursor(row_factory=dict_row) as cursor:
            await cursor.execute(
                query,
                params={
                    "owner": owner,
                    "repo": repo,
                    "since": since,
                    "until": until,
                },
            )
            return await cursor.fetchall()

    async def check_owner_exists(self, owner: str) -> bool:
        query = """
            SELECT 1
            FROM activity
            WHERE owner = %(owner)s;
            """
        async with self._con.cursor() as cursor:
            await cursor.execute(query, params={"owner": owner})
            res = await cursor.fetchone()
            return res is not None

    async def check_repo_exists(self, repo: str) -> bool:
        query = """
            SELECT 1
            FROM activity
            WHERE repo = %(repo)s;
            """
        async with self._con.cursor() as cursor:
            await cursor.execute(query, params={"repo": repo})
            res = await cursor.fetchone()
            return res is not None
