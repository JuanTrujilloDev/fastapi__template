"""

Dependencies for FastAPI application.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

import importlib
import logging
import os
import pkgutil
from typing import Callable

from fastapi import FastAPI

from fastapi__template.settings import SETTINGS

ALLOWED_ENGINES = {
    "sqlite": (f"sqlite:///{SETTINGS.DATABASE_NAME}"),
    "postgresql": (
        f"postgresql://{SETTINGS.DATABASE_USER}:{SETTINGS.DATABASE_PASSWORD}"
        f"@{SETTINGS.DATABASE_HOST}:{SETTINGS.DATABASE_PORT}"
    ),
    "mysql": (
        f"mysql://{SETTINGS.DATABASE_USER}:{SETTINGS.DATABASE_PASSWORD}"
        f"@{SETTINGS.DATABASE_HOST}:{SETTINGS.DATABASE_PORT}"
    ),
    "oracle": (
        f"oracle://{SETTINGS.DATABASE_USER}:{SETTINGS.DATABASE_PASSWORD}"
        f"@{SETTINGS.DATABASE_HOST}:{SETTINGS.DATABASE_PORT}"
    ),
    "mssql": (
        f"mssql://{SETTINGS.DATABASE_USER}:{SETTINGS.DATABASE_PASSWORD}"
        f"@{SETTINGS.DATABASE_HOST}:{SETTINGS.DATABASE_PORT}"
    ),
}


def install_apps(fastapi_app: FastAPI) -> list:
    """Install all apps automatically."""
    logger = logging.getLogger("uvicorn.error")
    for app in SETTINGS.INSTALLED_APPS:
        try:
            module_app = importlib.import_module(f"{app}.app")
            if hasattr(module_app, "register"):
                module_app.register(fastapi_app)
                logger.info("Registered app: %s", app)
            else:
                raise ValueError(f"There is no register method in your app module {app}.")
        except ModuleNotFoundError as e:
            raise ValueError(f"App module {app} not found {e}.") from e
        except Exception as e:
            raise ValueError(f"Error registering app {app} {e}.") from e


def find_models():
    """Find all models in the application."""
    for app in SETTINGS.INSTALLED_APPS:
        try:
            module_app = importlib.import_module(f"{app}.app")
            models = os.path.join(os.path.dirname(module_app.__file__), "models")
            for model in pkgutil.iter_modules([models]):
                model = importlib.import_module(f"{app}.models.{model.name}")
        except ModuleNotFoundError as e:
            raise ValueError(f"App module {app} not found {e}.") from e
        except Exception as e:
            raise ValueError(f"Error registering app {app} {e}.") from e


def customize_openapi(func: Callable[..., dict]) -> Callable[..., dict]:
    """Customize OpenAPI schema."""

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
