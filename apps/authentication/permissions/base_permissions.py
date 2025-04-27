from typing import Annotated

from fastapi import Depends, Request

from apps.authentication.constants.token_constants import OAUTH2_SCHEME
from apps.authentication.exceptions.permission_exceptions import CREDENTIALS_EXCEPTION
from apps.authentication.methods.token_util_methods import validate_bearer_token


async def is_authenticated(
    request: Request, bearer: Annotated[str, Depends(OAUTH2_SCHEME)]
) -> Request:
    """
    Middleware to check if the user is authenticated.

    Args:
        request (Request): The incoming request.
        call_next: The next middleware or route handler.

    Returns:
        Response: The response from the next middleware or route handler.
    """
    token = request.headers.get("Authorization", "")
    token = token.split("Bearer ")[-1]
    token = await validate_bearer_token(bearer)
    if token.user is None or not token.user.is_active:
        raise CREDENTIALS_EXCEPTION

    request.scope["user"] = token.user
    request.scope["access_token"] = token
    return request


async def is_staff(request: Request) -> Request:
    """
    Middleware to check if the user is a staff member.

    Args:
        request (Request): The incoming request.
        call_next: The next middleware or route handler.

    Returns:
        Response: The response from the next middleware or route handler.
    """
    if not request.user.is_staff:
        raise CREDENTIALS_EXCEPTION

    return request


async def is_superuser(request: Request) -> Request:
    """
    Middleware to check if the user is a superuser.

    Args:
        request (Request): The incoming request.
        call_next: The next middleware or route handler.

    Returns:
        Response: The response from the next middleware or route handler.
    """
    if not request.user.is_superuser:
        raise CREDENTIALS_EXCEPTION

    return request
