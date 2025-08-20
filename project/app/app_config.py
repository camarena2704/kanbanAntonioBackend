import logging
import os

from pydantic_settings import BaseSettings

logger = logging.getLogger(__name__)


class AppSettings(BaseSettings):
    api_version: str = os.getenv("API_VERSION")


def get_application_settings() -> AppSettings:
    logger.info("loading application settings")
    return AppSettings()


app_settings = get_application_settings()
