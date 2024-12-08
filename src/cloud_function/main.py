# import asyncio
# import time
# from typing import Any
# from src.cloud_function.fetcher import GitHubFetcher
# from src.cloud_function.parser import GitHubParser


# async def fetch_commits_for_repo(fetcher: GitHubFetcher, parser: GitHubParser, repo: dict[str, Any]) -> None:
#     """Функция для асинхронной обработки данных одного репозитория."""
#     try:
#         repo_name = repo["repo"]
#         owner = repo["owner"]

#         print(f"Fetching commits for {repo_name}...")
#         commits = await fetcher.get_commits(owner, repo_name)
#         parsed_commits = await parser.parse_commits(repo_name, owner, commits)

#         print(f"Commits for repository: {repo_name}")
#         for commit in parsed_commits:
#             print(f"  Author: {commit['author']}, Date: {commit['date']}")
#         print("-" * 50)
#     except Exception as e:
#         print(f"Error fetching commits for {repo['repo']}: {e}")


# async def main() -> None:
#     try:
#         # Инициализация классов для работы с API и парсинга
#         fetcher = GitHubFetcher()
#         parser = GitHubParser()

#         # Получение списка популярных репозиториев
#         repos = await fetcher.get_top_repos()
#         parsed_repos = await parser.parse_repo_data(repos)

#         # Вывод информации о репозиториях
#         print("Repositories:")
#         for repo in parsed_repos:
#             print(
#                 f"Name: {repo['repo']}, Owner: {repo['owner']}, Stars: {repo['stars']}"
#             )
#         print("-" * 50)

#         # Асинхронная обработка коммитов для всех репозиториев параллельно
#         await asyncio.gather(
#             *(fetch_commits_for_repo(fetcher, parser, repo) for repo in parsed_repos)
#         )

#     except Exception as e:
#         print(f"Error occurred: {e}")


# if __name__ == "__main__":
#     a = time.time()
#     asyncio.run(main())
#     print(f"Execution time: {time.time() - a:.2f} seconds")
