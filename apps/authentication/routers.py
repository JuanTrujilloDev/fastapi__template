"""
Authentication routers

This file contains all routers for the authentication app.

This files is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

from apps.authentication.views.login_views import login_router
from apps.authentication.views.refresh_views import refresh_router
from fastapi__template.app import app

app.include_router(login_router, prefix="/login", tags=["login"])
app.include_router(refresh_router, prefix="/refresh", tags=["refresh"])
