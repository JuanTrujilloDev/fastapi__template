"""

FastAPI application

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

from fastapi import FastAPI

from fastapi__template.dependencies import install_apps
from fastapi__template.settings import SETTINGS


def create_app() -> FastAPI:
    """Create FastAPI application."""
    fastapi_app = FastAPI(
        title=SETTINGS.app_name,
        description=SETTINGS.app_description,
        version=SETTINGS.app_version,
        terms_of_service=SETTINGS.terms_of_service,
        contact={
            "name": SETTINGS.app_author,
            "email": SETTINGS.app_author_email,
        },
        debug=SETTINGS.debug,
        redoc_url=SETTINGS.url_redocs,
        docs_url=SETTINGS.url_docs,
        openapi_url="/openapi.json",
    )

    return fastapi_app


app = create_app()
install_apps(app)
