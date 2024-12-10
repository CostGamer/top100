from psycopg_pool import AsyncConnectionPool

from src.cloud_function.fetcher import GitHubFetcher
from src.cloud_function.get_db import get_db_and_execute
from src.cloud_function.parser import GitHubParser

fetcher = GitHubFetcher()
parser = GitHubParser()


async def fetch_parse_push_to_db_repo(pool: AsyncConnectionPool) -> None:
    delete_query = """
    DELETE FROM top100
    WHERE repo = %(repo)s;
    """
    insert_query = """
    INSERT INTO top100 (
        repo, owner, position_cur, position_prev, stars, watchers, forks, open_issues, language
    )
    VALUES (
        %(repo)s, %(owner)s, %(position_cur)s, %(position_prev)s, %(stars)s,
        %(watchers)s, %(forks)s, %(open_issues)s, %(language)s
    )
    """
    get_query = """
    SELECT position_cur
    FROM top100
    WHERE repo = %(repo)s
    """

    try:
        repos = await fetcher.get_top_repos()
        if not repos:
            print("No repositories found.")
            return
    except Exception as e:
        print(f"Failed to fetch top repositories: {e}")
        return

    try:
        parsed_repos = await parser.parse_repo_data(repos)
    except Exception as e:
        print(f"Failed to parse repository data: {e}")
        return

    for repo_data in parsed_repos:
        try:
            position_prev_result = await get_db_and_execute(
                get_query,
                {"repo": repo_data["repo"]},
                pool,
            )
            position_prev = position_prev_result[0][0] if position_prev_result else None
            repo_data["position_prev"] = position_prev
        except Exception as e:
            print(f"Error fetching previous position for {repo_data['repo']}: {e}")
            repo_data["position_prev"] = None

        try:
            await get_db_and_execute(
                delete_query,
                {"repo": repo_data["repo"]},
                pool,
            )
        except Exception as e:
            print(f"Error deleting data for {repo_data['repo']}: {e}")

        try:
            await get_db_and_execute(
                insert_query,
                repo_data,
                pool,
            )
        except Exception as e:
            print(f"Error inserting data for {repo_data['repo']}: {e}")
