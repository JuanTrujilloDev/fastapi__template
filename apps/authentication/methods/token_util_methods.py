"""

Token Util Methods

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

from datetime import datetime, timedelta
from typing import Annotated
from uuid import UUID

import jwt
from fastapi import HTTPException, status
from fastapi.params import Depends
from fastapi_sqlalchemy import db

from apps.authentication.constants.token_constants import OAUTH2_SCHEME, TokenTypes
from apps.authentication.models.outstanding_token import OutstandingToken
from apps.users.models.user import User
from fastapi__template.settings import settings


def create_access_token(data: dict, user_id: UUID) -> str:
    """
    Create access token.

    Args:

    data: dict: Data to be stored in the token.
    user_id: UUID: User ID.

    Returns:

    str: Access token.
    """
    data["exp"] = datetime.now() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    token = jwt.encode(data, settings.SECRET_KEY, algorithm=settings.TOKEN_ALGORITHM)
    token = OutstandingToken(
        jti=token,
        token_type=TokenTypes.ACCESS,
        expires_at=(data["exp"]),
        user_id=user_id,
    )
    db.session.add(token)
    db.session.commit()
    return token.jti


def create_refresh_token(data: dict, user_id: UUID) -> str:
    """
    Create refresh token.

    Args:

    data: dict: Data to be stored in the token.
    user_id: UUID: User ID.

    Returns:

    str: Refresh token.
    """
    data["exp"] = datetime.now() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    token = jwt.encode(data, settings.SECRET_KEY, algorithm=settings.TOKEN_ALGORITHM)
    token = OutstandingToken(
        jti=token,
        token_type=TokenTypes.REFRESH,
        expires_at=(data["exp"]),
        user_id=user_id,
    )
    db.session.add(token)
    db.session.commit()
    return token.jti


def get_current_user(token: Annotated[str, Depends(OAUTH2_SCHEME)]) -> User:
    """
    Verify access token.

    Args:

    token: str: Token to be verified.

    Returns:

    bool: True if token is valid, False otherwise.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        data = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.TOKEN_ALGORITHM]
        )
        token = (
            db.session.query(OutstandingToken)
            .filter_by(jti=token, token_type=TokenTypes.ACCESS)
            .first()
        )
        if not token or not token.is_active:
            raise credentials_exception

        username = data.get("sub", None)
        user = db.session.query(User).filter_by(email=username).first()
        if user is None or not user.is_active:
            raise credentials_exception

        return user
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError) as e:
        raise credentials_exception from e
