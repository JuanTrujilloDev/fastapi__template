"""

Admin file

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

from apps.authentication.models.api_key import APIKey
from apps.authentication.models.blacklisted_token import BlacklistedToken
from apps.authentication.models.outstanding_token import OutstandingToken
from fastapi__template.admin.base_admin_views import BaseModelAdminView
from fastapi__template.admin.site import register


@register()
class ApiKeyAdmin(BaseModelAdminView, model=APIKey):
    """Model view for APIKey model"""

    column_list = [APIKey.id, APIKey.title]


@register()
class OutstandingTokenAdmin(BaseModelAdminView, model=OutstandingToken):
    """Model view for OutstandingToken model"""

    column_list = [
        OutstandingToken.id,
        OutstandingToken.jti,
        OutstandingToken.token_type,
        OutstandingToken.expires_at,
        OutstandingToken.revoked,
        OutstandingToken.revoked_at,
        OutstandingToken.user_id,
    ]


@register()
class BlacklistedTokenAdmin(BaseModelAdminView, model=BlacklistedToken):
    """Model view for BlacklistedToken model"""

    column_list = [
        BlacklistedToken.id,
        BlacklistedToken.outstanding_token_id,
    ]
