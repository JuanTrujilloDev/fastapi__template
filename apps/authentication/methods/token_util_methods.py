"""

Token Util Methods

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

from datetime import datetime, timedelta, timezone
from uuid import UUID

import jwt
from fastapi_sqlalchemy import db

from apps.authentication.constants.token_constants import TokenTypes
from apps.authentication.exceptions.permission_exceptions import CREDENTIALS_EXCEPTION
from apps.authentication.models.outstanding_token import OutstandingToken
from apps.users.models.user import User
from fastapi__template.settings import settings


def create_access_token(data: dict, user_id: UUID, client: str) -> str:
    """
    Create access token.

    Args:

    data: dict: Data to be stored in the token.
    user_id: UUID: User ID.

    Returns:

    str: Access token.
    """
    data["exp"] = datetime.now(tz=timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    token = jwt.encode(data, settings.SECRET_KEY, algorithm=settings.TOKEN_ALGORITHM)
    token = OutstandingToken(
        jti=token,
        token_type=TokenTypes.ACCESS,
        expires_at=(data["exp"]),
        user_id=user_id,
        client=client,
    )
    db.session.add(token)
    db.session.commit()
    return token.jti


def create_refresh_token(data: dict, user_id: UUID, client: str) -> str:
    """
    Create refresh token.

    Args:

    data: dict: Data to be stored in the token.
    user_id: UUID: User ID.

    Returns:

    str: Refresh token.
    """
    data["exp"] = datetime.now(tz=timezone.utc) + timedelta(
        days=settings.REFRESH_TOKEN_EXPIRE_DAYS
    )
    token = jwt.encode(data, settings.SECRET_KEY, algorithm=settings.TOKEN_ALGORITHM)
    token = OutstandingToken(
        jti=token,
        token_type=TokenTypes.REFRESH,
        expires_at=(data["exp"]),
        user_id=user_id,
        client=client,
    )
    db.session.add(token)
    db.session.commit()
    return token.jti


def clear_user_tokens(user: User, client: str = None) -> None:
    """
    Clear user tokens.

    Args:

    user: User: User object.
    client_id: str: Client ID to filter tokens. If None, all tokens will be cleared.
    """
    outstanding_tokens = db.session.query(OutstandingToken).filter_by(user_id=user.id)
    if client:
        outstanding_tokens = outstanding_tokens.filter_by(client=client)

    outstanding_tokens.update(
        {
            OutstandingToken.revoked: True,
            OutstandingToken.expires_at: datetime.now(tz=timezone.utc),
        }
    )
    db.session.commit()


async def validate_bearer_token(token: str) -> OutstandingToken:
    """
    Verify access token.

    Args:

    token: str: Token to be verified.

    Returns:

    bool: True if token is valid, False otherwise.
    """
    try:
        jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.TOKEN_ALGORITHM],
            options={"verify_exp": False},
        )
        token = (
            db.session.query(OutstandingToken)
            .filter_by(jti=token, token_type=TokenTypes.ACCESS)
            .first()
        )
        if not token or not token.is_valid:
            raise CREDENTIALS_EXCEPTION

        return token
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError) as e:
        raise CREDENTIALS_EXCEPTION from e
