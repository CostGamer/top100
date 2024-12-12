from datetime import date as set_date

from psycopg import AsyncConnection
from psycopg.rows import dict_row


class CommitGateway:
    def __init__(self, con: AsyncConnection) -> None:
        self._con = con

    async def get_commit_activity_per_day(
        self,
        owner: str,
        repo: str,
        date: set_date,
    ) -> dict | None:
        query = """
            SELECT date, commits, authors
            FROM activity
            WHERE owner = %(owner)s
            AND repo = %(repo)s
            AND date = %(date)s;
            """
        async with self._con.cursor(row_factory=dict_row) as cursor:
            await cursor.execute(
                query,
                params={
                    "owner": owner,
                    "repo": repo,
                    "date": date,
                },
            )
            return await cursor.fetchone()

    async def check_owner_exists(self, owner: str) -> bool:
        query = """
            SELECT 1
            FROM top100
            WHERE owner = %(owner)s;
            """
        async with self._con.cursor() as cursor:
            await cursor.execute(query, params={"owner": owner})
            res = await cursor.fetchone()
            return res is not None

    async def check_repo_exists(self, repo: str) -> bool:
        query = """
            SELECT 1
            FROM top100
            WHERE repo = %(repo)s;
            """
        async with self._con.cursor() as cursor:
            await cursor.execute(query, params={"repo": repo})
            res = await cursor.fetchone()
            return res is not None

    async def push_data_for_exact_date_to_db(
        self,
        owner: str,
        repo: str,
        date: set_date,
        commits: int,
        authors: list[str],
    ) -> None:
        query = """
            INSERT INTO activity (owner, repo, date, commits, authors)
            VALUES (%(owner)s, %(repo)s, %(date)s, %(commits)s, %(authors)s)
            """

        async with self._con.cursor() as cursor:
            await cursor.execute(
                query,
                params={
                    "owner": owner,
                    "repo": repo,
                    "date": date,
                    "commits": commits,
                    "authors": authors,
                },
            )

    async def update_commits_data_today(
        self,
        owner: str,
        repo: str,
        date: set_date,
        commits: int,
        authors: list[str],
    ) -> None:
        query = """
            UPDATE activity
            SET commits = %(commits)s,
                authors = %(authors)s
            WHERE owner = %(owner)s
                AND repo = %(repo)s
                AND date = %(date)s;
            """
        async with self._con.cursor() as cursor:
            await cursor.execute(
                query,
                params={
                    "owner": owner,
                    "repo": repo,
                    "date": date,
                    "commits": commits,
                    "authors": authors,
                },
            )
