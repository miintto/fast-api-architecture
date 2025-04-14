from functools import lru_cache
import os
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = str(Path(__file__).parents[2])


class Settings(BaseSettings):
    APP_ENV: str
    BASE_DIR: str = BASE_DIR
    DEBUG: bool = os.getenv("APP_ENV") not in ("production", "test")

    SECRET_KEY: str

    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    SQLALCHEMY_POOL_SIZE: int = 100

    model_config = SettingsConfigDict(env_file=".env")


@lru_cache()
def get_settings() -> Settings:
    return Settings()
