from fastapi import APIRouter
from fastapi_utils.cbv import cbv

from apps.authentication.schemas.refresh_schemas import RefreshTokenSchema

refresh_router = APIRouter()


@cbv(refresh_router)
class RefreshViews:
    """Refresh views."""

    @refresh_router.post("/", response_model=dict)
    async def refresh(self, refresh_token_schema: RefreshTokenSchema):
        """Refresh endpoint."""
        return {"access_token": refresh_token_schema.refresh_access_token()}
