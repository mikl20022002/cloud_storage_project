from pydantic_settings import BaseSettings, SettingsConfigDict


class DbSettings(BaseSettings):
    DB_USER: str
    DB_PASS: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    def async_db_url(self):
        return f"postgres+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class ServerSettings(BaseSettings):
    SERVER_HOST: str
    SERVER_PORT: int

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


db_settings = DbSettings()
server_settings = ServerSettings()

