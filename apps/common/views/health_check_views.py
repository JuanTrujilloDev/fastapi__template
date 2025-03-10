"""

Health check views

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

from fastapi_utils.cbv import cbv

from apps.common.routers import health_check_router


@cbv(health_check_router)
class HealthCheckViews:
    """Health check views."""

    @health_check_router.get("/", response_model=dict)
    async def health_check(self):
        """Health check endpoint."""
        return {"status": "ok"}
