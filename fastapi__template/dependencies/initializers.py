"""

Initializer helper methods.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

import importlib
import logging
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
    if not hasattr(module_app, "register"):
        raise ValueError(f"There is no register method in your app module {app}.")

    module_app.register(fastapi_app)
    find_routers(fastapi_app, app)
    logger.info("App %s is installed.", app)


def find_routers(fastapi_app: FastAPI, app: str) -> list:
    """Find routers in the app."""
    try:
        module_app = importlib.import_module(f"{app}.routers")
    except ModuleNotFoundError:
        return
    else:
        routers = getattr(module_app, "routers", [])
        for router in routers:
            fastapi_app.include_router(router)


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
