"""

Users app module

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

from fastapi import FastAPI

from apps.users.models.user import User


def register(app: FastAPI):
    """Register app instance."""
    # Models to be included in the database
    app.registered_models += [User]
    return app
