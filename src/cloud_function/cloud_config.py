import os


def get_env_variable(name: str) -> str:
    value = os.getenv(name)
    if value is None:
        raise ValueError(f"ENV {name} was not found")
    return value


def build_db_uri() -> str:
    db_user = get_env_variable("DB_USER")
    db_password = get_env_variable("DB_PASSWORD")
    db_host = get_env_variable("DB_HOST")
    db_port = get_env_variable("DB_PORT")
    db_name = get_env_variable("DB_NAME")
    return f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"


GITHUB_API_URL_REPO = "https://api.github.com/search/repositories"
GH_TOKEN = get_env_variable("GH_TOKEN")
DB_URI = build_db_uri()

HEADERS = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {GH_TOKEN}",
}
REPO_PARAMS = {
    "q": "stars:>1",  # Фильтрация репозиториев по звёздам больше 1
    "sort": "stars",
    "order": "desc",
    "per_page": 100,
}
