from pydantic_settings import BaseSettings, SettingsConfigDict

VALID_PARAMS = (
    "repo",
    "owner",
    "position_cur",
    "position_prev",
    "stars",
    "watchers",
    "forks",
    "open_issues",
    "language",
)


class DatabaseSettings(BaseSettings):
    DB_HOST: str = "127.0.0.1"
    DB_PORT: int = 5432
    DB_NAME: str = "db"
    DB_USER: str = "test_user"
    DB_PASSWORD: str = "test_pass"
    DATABASE_URL: str | None = None

    @property
    def db_uri(self) -> str:
        return (
            self.DATABASE_URL
            or f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )


class LoggingSettings(BaseSettings):
    LOG_LEVEL: str = "DEBUG"
    LOG_FILE: str = "app.log"
    LOG_ENCODING: str = "utf-8"


class GHTokenSettings(BaseSettings):
    GH_TOKEN: str = "test_token"

    @property
    def headers(self) -> dict:
        return {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {self.GH_TOKEN}",
        }

    @property
    def github_api_url(self) -> str:
        return "https://api.github.com/repos"


class Settings(
    DatabaseSettings,
    LoggingSettings,
    GHTokenSettings,
):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


all_settings = Settings()
