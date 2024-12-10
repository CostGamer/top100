from src.backend.DB.settings import all_settings

GITHUB_API_URL_REPO = "https://api.github.com/search/repositories"
GITHUB_API_URL_COMMITS = "https://api.github.com"
HEADERS = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {all_settings.GH_TOKEN}",
}
REPO_PARAMS = {
    "q": "stars:>1",  # Фильтрация репозиториев по звездами больше 1
    "sort": "stars",  # Сортировка по звездами
    "order": "desc",  # По убыванию
    "per_page": 100,  # Ограничение на 100 репозиториев
}

DB_URI = all_settings.db_uri
