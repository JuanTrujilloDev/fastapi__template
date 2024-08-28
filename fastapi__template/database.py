"""

Database module.

This module is used to set up the database.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

import importlib
import os
import pkgutil

from sqlmodel import create_engine

from fastapi__template.settings import SETTINGS


def get_engine():
    """Get database engine."""
    if SETTINGS.database_engine == "sqlite":
        return create_engine(SETTINGS.database_url, echo=True)
    elif SETTINGS.database_engine == "postgresql":
        return create_engine(SETTINGS.database_url, echo=True, pool_pre_ping=True)
    elif SETTINGS.database_engine == "mysql":
        return create_engine(SETTINGS.database_url, echo=True, pool_pre_ping=True)
    else:
        raise ValueError("Invalid database engine specified in settings.")


def find_models():
    """Find all models in the application."""
    for app in SETTINGS.installed_apps:
        try:
            module_app = importlib.import_module(f"{app}.app")
            models = os.path.join(os.path.dirname(module_app.__file__), "models")
            for model in pkgutil.iter_modules([models]):
                model = importlib.import_module(f"{app}.models.{model.name}")
        except ModuleNotFoundError as e:
            raise ValueError(f"App module {app} not found {e}.") from e
        except Exception as e:
            raise ValueError(f"Error registering app {app} {e}.") from e
