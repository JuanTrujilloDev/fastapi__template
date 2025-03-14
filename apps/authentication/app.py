"""

Authentication app module

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

from fastapi import FastAPI

from apps.authentication.models.api_key import APIKey
from apps.authentication.models.outstanding_token import OutstandingToken


def register(app: FastAPI):
    """Register app instance."""
    # Include models
    app.registered_models += [OutstandingToken, APIKey]
    return app
