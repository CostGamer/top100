from psycopg_pool import AsyncConnectionPool

from src.cloud_function.fetcher import GitHubFetcher
from src.cloud_function.get_db import get_db_and_execute
from src.cloud_function.parser import GitHubParser

fetcher = GitHubFetcher()
parser = GitHubParser()


async def fetch_parse_push_to_db_repo(pool: AsyncConnectionPool) -> None:
    query = """
        INSERT INTO top100 (
            repo, owner, position_cur, position_prev, stars, watchers, forks, open_issues, language
        )
        VALUES (
            %(repo)s, %(owner)s, %(position_cur)s, %(position_prev)s, %(stars)s,
            %(watchers)s, %(forks)s, %(open_issues)s, %(language)s
        )
    """

    try:
        repos = await fetcher.get_top_repos()
    except Exception as e:
        print(f"Failed to fetch top repositories: {e}")
        return

    if not repos:
        print("No repositories found.")
        return

    parsed_repos = await parser.parse_repo_data(repos)

    for repo_data in parsed_repos:
        try:
            await get_db_and_execute(
                query,
                repo_data,
                pool,
            )
        except Exception as e:
            print(f"Unexpacted error {e}")
