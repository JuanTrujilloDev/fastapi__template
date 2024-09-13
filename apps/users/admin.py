"""

admin file

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

from sqladmin import ModelView

from apps.users.models.user import User


class UserAdmin(ModelView, model=User):
    """Model view for User Admin model"""

    column_list = [User.id, User.name]
