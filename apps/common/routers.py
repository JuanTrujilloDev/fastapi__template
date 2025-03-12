"""

Routers for common app

This file contains all routers for the common app.

This files is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

from apps.common.views.health_check_views import health_check_router
from fastapi__template.app import app

app.router.include_router(
    health_check_router, tags=["Health Check"], prefix="/health-check"
)
