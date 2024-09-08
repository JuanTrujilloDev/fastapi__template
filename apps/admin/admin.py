"""

admin file

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

from sqladmin import ModelView

from apps.admin.models.user import User


class UserAdmin(ModelView, model=User):
    """
    Admin view for managing User model.

    Attributes:
        column_list (list): List of columns to display in the admin view.
    """

    column_list = [User.id, User.name]
