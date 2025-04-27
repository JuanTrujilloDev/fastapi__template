from fastapi import APIRouter, Depends, Request
from fastapi_utils.cbv import cbv

from apps.authentication.methods.token_util_methods import clear_user_tokens
from apps.authentication.permissions.base_permissions import (
    is_authenticated,
)

logout_router = APIRouter()


@cbv(logout_router)
class LogoutViews:
    """Logout views."""

    @logout_router.post(
        "/",
        response_model=dict,
        status_code=200,
        dependencies=[Depends(is_authenticated)],
    )
    async def logout(self, request: Request):
        """Logout endpoint."""
        access_token = request.scope["access_token"]
        clear_user_tokens(request.user, access_token.client)
        return {"message": "Logged out successfully"}
