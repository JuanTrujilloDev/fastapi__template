"""

Admin file

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

from apps.authentication.models.api_key import APIKey
from fastapi__template.admin import register
from fastapi__template.admin.base_admin_views import BaseModelAdminView


@register()
class ApiKeyAdmin(BaseModelAdminView, model=APIKey):
    """Model view for APIKey model"""

    column_list = [APIKey.id, APIKey.title]
