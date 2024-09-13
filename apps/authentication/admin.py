"""

Admin file

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

from sqladmin import ModelView

from apps.authentication.models.api_key import APIKey


class ApiKeyAdmin(ModelView, model=APIKey):
    """Model view for APIKey model"""

    column_list = [APIKey.id, APIKey.title]
