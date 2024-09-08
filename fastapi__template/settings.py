"""
Config file for fastapi__template application.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

import os
from typing import ClassVar, List

from pydantic_settings import BaseSettings

from fastapi__template.database import get_engine
from fastapi__template.load_env import load_env


class Settings(BaseSettings):
    """Application settings."""

    load_env()

    # Secret Key
    SECRET_KEY: str = os.getenv("SECRET_KEY")

    # APP Details
    APP_NAME: str = os.getenv("APP_NAME", "FastAPI Template")
    APP_DESCRIPTION: str = os.getenv("APP_DESCRIPTION", "FastAPI template application.")
    APP_VERSION: str = os.getenv("APP_VERSION", "0.1.0")
    APP_AUTHOR: str = os.getenv("APP_AUTHOR", "Author Name")
    APP_AUTHOR_EMAIL: str = os.getenv("APP_AUTHOR_EMAIL", "test@test.com")
    APP_TERMS_OF_SERVICE: str = os.getenv("TERMS_OF_SERVICE", "http://localhost:8000")

    # Server Settings
    DEBUG: bool = os.getenv("DEBUG", False)
    PORT: int = os.getenv("PORT", 8000)
    HOST: str = os.getenv("HOST", "127.0.0.1")
    RELOAD: bool = os.getenv("RELOAD", False)
    URL_DOCS: str = os.getenv("URL_DOCS", "/docs")
    URL_REDOCS: str = os.getenv("URL_REDOCS", "/redocs")

    # Installed apps
    INSTALLED_APPS: list = ["apps.common", "apps.authentication", "apps.admin"]

    # Database Settings
    DATABASE_HOST: str = os.getenv("DATABASE_HOST", "localhost")
    DATABASE_PORT: str = os.getenv("DATABASE_PORT", "5432")
    DATABASE_NAME: str = os.getenv("DATABASE_NAME", "fastapi_template")
    DATABASE_USER: str = os.getenv("DATABASE_USER", "fastapi_template")
    DATABASE_PASSWORD: str = os.getenv("DATABASE_PASSWORD", "fastapi_template")
    DATABASE_ENGINE_NAME: str = os.getenv("DATABASE_ENGINE", "postgresql")
    DATABASE_ENGINE: str = get_engine(
        database_engine=DATABASE_ENGINE_NAME,
        database_name=DATABASE_NAME,
        database_user=DATABASE_USER,
        database_password=DATABASE_PASSWORD,
        database_host=DATABASE_HOST,
        database_port=DATABASE_PORT,
    )
    DATABASE_URL: ClassVar[str] = DATABASE_ENGINE + "/" + DATABASE_NAME

    # CORS AND SECURITY
    ALLOW_ORIGINS: List[str] = os.getenv("ALLOW_ORIGINS", ["*"])
    ALLOW_CREDENTIALS: bool = os.getenv("ALLOW_CREDENTIALS", True)


SETTINGS = Settings()
