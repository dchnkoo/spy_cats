from pydantic_settings import SettingsConfigDict, BaseSettings
import pydantic as _p

from pathlib import Path


APP_DIR = Path(__file__).parent

ROOT_DIR = APP_DIR.parent


config = SettingsConfigDict(env_file=ROOT_DIR / ".env")


class PostgresSettings(BaseSettings):
    model_config = config

    host: str = _p.Field("localhost", alias="postgres_host")
    port: int = _p.Field(5432, alias="postgres_port")
    database: str = _p.Field(..., alias="postgres_db")
    user: str = _p.Field(..., alias="postgres_user")
    password: str = _p.Field(..., alias="postgres_password")

    @property
    def dsn(self):
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"

    @property
    def async_dsn(self):
        return self.dsn.replace("postgresql", "postgresql+asyncpg")


postgres = PostgresSettings()
