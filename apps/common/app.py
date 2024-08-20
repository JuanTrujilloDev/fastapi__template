"""

Common app module

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

from fastapi import FastAPI

from apps.common.views.health_check_views import health_check_router


def register(app: FastAPI):
    """Register app instance."""
    app.include_router(health_check_router)
    return app
