"""

FastAPI application

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi_sqlalchemy import DBSessionMiddleware
from pydantic import ValidationError
from sqlmodel import StaticPool, create_engine

from apps.exceptions.handlers.pydantic_validation_error_handler import (
    pydantic_validation_error_handler,
)
from apps.exceptions.handlers.request_validation_error_handler import (
    request_validation_error_handler,
)
from fastapi__template.dependencies.initializers import install_apps
from fastapi__template.settings import settings


def __create_app() -> FastAPI:
    """Create FastAPI application."""
    fastapi_app = FastAPI(
        title=settings.APP_NAME,
        description=settings.APP_DESCRIPTION,
        version=settings.APP_TERMS_OF_SERVICE,
        terms_of_service=settings.APP_TERMS_OF_SERVICE,
        contact={
            "name": settings.APP_AUTHOR,
            "email": settings.APP_AUTHOR_EMAIL,
        },
        debug=settings.DEBUG,
        redoc_url=settings.URL_REDOCS,
        docs_url=settings.URL_DOCS,
        openapi_url="/openapi.json",
    )
    fastapi_app.config = settings
    fastapi_app.registered_models = []
    fastapi_app.routers = []

    # Add middlewares
    fastapi_app.add_middleware(DBSessionMiddleware, db_url=settings.DATABASE_URL)
    fastapi_app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOW_ORIGINS,
        allow_credentials=settings.ALLOW_CREDENTIALS,
    )
    fastapi_app.default_engine = create_engine(
        settings.DATABASE_URL, poolclass=StaticPool
    )

    # TODO: Add custom exception handlers
    fastapi_app.exception_handlers = {
        RequestValidationError: request_validation_error_handler,
        ValidationError: pydantic_validation_error_handler,
    }
    return fastapi_app


app = __create_app()
app.apps = install_apps(app)
