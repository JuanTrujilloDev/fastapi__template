"""

FastAPI application

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_sqlalchemy import DBSessionMiddleware
from fastapi_utils import Api
from sqladmin import Admin

from fastapi__template.dependencies import DEFAULT_ENGINE, install_apps
from fastapi__template.settings import SETTINGS


def __create_app() -> FastAPI:
    """Create FastAPI application."""
    fastapi_app = FastAPI(
        title=SETTINGS.APP_NAME,
        description=SETTINGS.APP_DESCRIPTION,
        version=SETTINGS.APP_TERMS_OF_SERVICE,
        terms_of_service=SETTINGS.APP_TERMS_OF_SERVICE,
        contact={
            "name": SETTINGS.APP_AUTHOR,
            "email": SETTINGS.APP_AUTHOR_EMAIL,
        },
        debug=SETTINGS.DEBUG,
        redoc_url=SETTINGS.URL_REDOCS,
        docs_url=SETTINGS.URL_DOCS,
        openapi_url="/openapi.json",
    )
    fastapi_app.config = SETTINGS
    fastapi_app.urls = Api(app=fastapi_app)

    # Add middlewares
    fastapi_app.add_middleware(DBSessionMiddleware, db_url=SETTINGS.DATABASE_URL)
    fastapi_app.add_middleware(
        CORSMiddleware,
        allow_origins=SETTINGS.ALLOW_ORIGINS,
        allow_credentials=SETTINGS.ALLOW_CREDENTIALS,
    )

    # Admin settings
    fastapi_app.default_admin = Admin(fastapi_app, DEFAULT_ENGINE)

    return fastapi_app


app = __create_app()
app.apps = install_apps(app)
