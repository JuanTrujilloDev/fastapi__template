"""
Config file for fastapi__template application.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

import os
from typing import List, ClassVar

from pydantic_settings import BaseSettings

from fastapi__template.load_env import load_env


class Settings(BaseSettings):
    """Application settings."""

    secret_key: str = os.getenv("SECRET_KEY")
    app_name: str = os.getenv("APP_NAME", "FastAPI Template")
    app_description: str = os.getenv("APP_DESCRIPTION", "FastAPI template application.")
    app_version: str = os.getenv("APP_VERSION", "0.1.0")
    app_author: str = os.getenv("APP_AUTHOR", "Author Name")
    app_author_email: str = os.getenv("APP_AUTHOR_EMAIL", "test@test.com")
    debug: bool = os.getenv("DEBUG", False)
    debug: bool = os.getenv("DEBUG", False)
    port: int = os.getenv("PORT", 8000)
    host: str = os.getenv("HOST", "127.0.0.1")
    reload: bool = os.getenv("RELOAD", False)
    url_docs: str = os.getenv("URL_DOCS", "/docs")
    url_redocs: str = os.getenv("URL_REDOCS", "/redocs")
    terms_of_service: str = os.getenv("TERMS_OF_SERVICE", "http://localhost:8000")
    installed_apps: list = ["apps.common", "apps.authentication"]
    database_host: str = os.getenv("DATABASE_HOST", "localhost")
    database_port: str = os.getenv("DATABASE_PORT", "5432")
    database_name: str = os.getenv("DATABASE_NAME", "fastapi_template")
    database_user: str = os.getenv("DATABASE_USER", "fastapi_template")
    database_password: str = os.getenv("DATABASE_PASSWORD", "fastapi_template")
    database_engine: str = os.getenv("DATABASE_ENGINE", "postgresql")
    database_url: ClassVar[str] = (
        f"postgresql://{database_user}:{database_password}@"
        f"{database_host}:{database_port}/{database_name}"
    )
    allow_origins: List[str] = os.getenv("ALLOW_ORIGINS", ["*"])


load_env()
SETTINGS = Settings()
