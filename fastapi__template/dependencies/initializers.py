"""

Initializer helper methods.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

import importlib
import logging
import os
import pkgutil
from typing import Callable

from fastapi import FastAPI

from fastapi__template.dependencies.handle_initializer_error import (
    handle_initializer_error,
)
from fastapi__template.settings import settings


def install_apps(fastapi_app: FastAPI) -> list:
    """Install all apps automatically."""
    logger = logging.getLogger("uvicorn.error")
    logger.info("Installing apps.")
    list(map(lambda app: register_app(fastapi_app, app), settings.INSTALLED_APPS))
    logger.info("All apps are installed.")
    return settings.INSTALLED_APPS


@handle_initializer_error
def register_app(fastapi_app: FastAPI, app: str) -> None:
    """Register an app."""
    logger = logging.getLogger("uvicorn.error")
    module_app = importlib.import_module(f"{app}.app")
    if hasattr(module_app, "register"):
        module_app.register(fastapi_app)
        find_app_model(app)
        logger.info("App %s is installed.", app)
    else:
        raise ValueError(f"There is no register method in your app module {app}.")


def find_app_model(app):
    """Find all models in the application."""
    module_app = importlib.import_module(f"{app}.app")
    models = os.path.join(os.path.dirname(module_app.__file__), "models")
    for model in pkgutil.iter_modules([models]):
        model = importlib.import_module(f"{app}.models.{model.name}")


def customize_openapi(func: Callable[..., dict]) -> Callable[..., dict]:
    """
    Customize OpenAPI schema.

    Allow to remove the 422 response from the OpenAPI schema.
    """

    def wrapper(*args, **kwargs) -> dict:
        """Wrapper."""
        res = func(*args, **kwargs)
        for _, method_item in res.get("paths", {}).items():
            for _, params in method_item.items():
                responses = params.get("responses")

                if "422" in responses and responses["422"]["content"]["application/json"][
                    "schema"
                ]["$ref"].endswith("HTTPValidationError"):
                    del responses["422"]

    return wrapper
