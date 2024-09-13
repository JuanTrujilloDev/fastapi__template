"""

admin file

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

from apps.users.models.user import User
from fastapi__template.admin import register
from fastapi__template.admin.base_admin_views import BaseModelAdminView


@register()
class UserAdmin(BaseModelAdminView, model=User):
    """Model view for User Admin model"""

    column_list = [User.id, User.name]
