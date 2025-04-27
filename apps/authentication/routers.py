"""
Authentication routers

This file contains all routers for the authentication app.

This files is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

from fastapi import APIRouter

from apps.authentication.views.login_views import login_router
from apps.authentication.views.logout_views import logout_router
from apps.authentication.views.refresh_views import refresh_router
from fastapi__template.app import app

authentication_router = APIRouter(
    prefix="/authentication",
    tags=["authentication"],
)

authentication_router.include_router(login_router, prefix="/login")
authentication_router.include_router(logout_router, prefix="/logout")
authentication_router.include_router(refresh_router, prefix="/refresh")
app.include_router(authentication_router)
