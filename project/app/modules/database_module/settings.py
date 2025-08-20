import os
from functools import lru_cache

from pydantic_settings import BaseSettings


class DatabaseSettings(BaseSettings):
    database_url: str = os.getenv("DATABASE_URL")


@lru_cache
def get_module_settings() -> DatabaseSettings:
    return DatabaseSettings()


module_settings = get_module_settings()

__all__ = ["module_settings"]
