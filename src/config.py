# moneyflow/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal


class Settings(BaseSettings):
    # === База данных ===
    DB_HOST: str = 'localhost'
    DB_PORT: int = 5432
    DB_USER: str = 'moneyflow'
    DB_PASS: str = 'moneyflow'
    DB_NAME: str = 'moneyflow_db'

    # === Приложение ===
    APP_NAME: str = 'MoneyFlow'
    DEBUG: bool = True

    # Какой драйвер использовать
    DB_DRIVER: Literal['asyncpg', 'psycopg'] = 'asyncpg'

    @property
    def database_url(self) -> str:
        """Для Alembic и sync-подключений (psycopg)"""
        return f'postgresql://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'

    @property
    def database_url_asyncpg(self) -> str:
        """Для async SQLAlchemy"""
        return f'postgresql+{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        case_sensitive=False,
        extra='ignore',
    )


settings = Settings()