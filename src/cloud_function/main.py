from src.cloud_function.fetcher import GitHubRepoFetcher
from src.cloud_function.parser import GitHubRepoParser


def main() -> None:
    try:
        fetcher = GitHubRepoFetcher()
        parser = GitHubRepoParser()

        repos = fetcher.get_top_repos()
        parsed_repos = parser.parse_repo_data(repos)

        for repo in parsed_repos:
            print(repo)
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
