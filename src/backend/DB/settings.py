from pydantic_settings import BaseSettings, SettingsConfigDict


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


# class DatabaseSettingsTest(BaseSettings):
#     DB_HOST_TEST: str = "127.0.0.1"
#     DB_PORT_TEST: int = 5432
#     DB_NAME_TEST: str = "db_test"
#     DB_USER_TEST: str = "test_user"
#     DB_PASSWORD_TEST: str = "test_pass"
#     DATABASE_URL_TEST: str | None = None

#     @property
#     def db_uri_test(self) -> str:
#         return (
#             self.DATABASE_URL_TEST
#             or f"postgresql://{self.DB_USER_TEST}:{self.DB_PASSWORD_TEST}@{self.DB_HOST_TEST}:{self.DB_PORT_TEST}/{self.DB_NAME_TEST}"
#         )


class LoggingSettings(BaseSettings):
    LOG_LEVEL: str = "DEBUG"
    LOG_FILE: str = "app.log"
    LOG_ENCODING: str = "utf-8"


class GHTokenSettings(BaseSettings):
    GH_TOKEN: str = "test_token"


class Settings(
    DatabaseSettings,
    LoggingSettings,
    GHTokenSettings,
):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


all_settings = Settings()
