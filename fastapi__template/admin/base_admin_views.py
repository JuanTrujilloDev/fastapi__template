"""

Base Admin View

This file contains the base admin view used to register sqlmodel models with the admin.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

from typing import Any

from fastapi import Request
from sqladmin import BaseView, ModelView

from fastapi__template.admin.query_helper import SQLModelQueryHelper


class BaseModelAdminView(ModelView):
    """Base Admin View for registering sqlmodel models with the admin."""

    async def insert_model(self, request: Request, data: dict) -> Any:
        return await SQLModelQueryHelper(self).insert(data, request)


class BaseAdminView(BaseView):
    """Base Admin View for custom implementations."""
