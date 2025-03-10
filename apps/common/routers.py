"""

Routers for common app

This file contains all routers for the common app.

This files is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

from fastapi import APIRouter

health_check_router = APIRouter(tags=["Health Check"], prefix="/health-check")
