"""

Routers for users app

This file contains all routers for the users app.

This files is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

from apps.users.views.user_views import user_router
from fastapi__template.app import app

app.include_router(user_router, prefix="/users", tags=["users"])
