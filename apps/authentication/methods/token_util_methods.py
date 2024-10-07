"""

Token Util Methods

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

from datetime import timedelta
from uuid import UUID

from fastapi_jwt import (
    JwtAccessBearer,
    JwtRefreshBearer,
)

from apps.authentication.constants.token_constants import TokenTypes
from apps.authentication.models.outstanding_token import OutstandingToken
from fastapi__template.settings import SETTINGS


def create_access_token(data: dict, user_id: UUID) -> str:
    """
    Create access token.

    Args:

    data: dict: Data to be stored in the token.
    user_id: UUID: User ID.

    Returns:

    str: Access token.
    """
    token = JwtAccessBearer(SETTINGS.SECRET_KEY).create_access_token(
        data, expires_delta=timedelta(minutes=SETTINGS.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    OutstandingToken(
        jti=token["jti"],
        token_type=TokenTypes.ACCESS,
        expires_at=token["exp"],
        user_id=user_id,
    )
    return token


def create_refresh_token(data: dict, user_id: UUID) -> str:
    """
    Create refresh token.

    Args:

    data: dict: Data to be stored in the token.
    user_id: UUID: User ID.

    Returns:

    str: Refresh token.
    """
    token = JwtRefreshBearer(SETTINGS.SECRET_KEY).create_refresh_token(
        data, expires_delta=timedelta(days=SETTINGS.REFRESH_TOKEN_EXPIRE_DAYS)
    )
    OutstandingToken(
        jti=token["jti"],
        token_type=TokenTypes.REFRESH,
        expires_at=token["exp"],
        user_id=user_id,
    )
    return token
