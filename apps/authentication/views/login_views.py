import uuid

from fastapi import APIRouter, Depends, Request
from fastapi_utils.cbv import cbv

from apps.authentication.forms.token_forms import (
    OAuth2EmailPasswordRequestForm,
)
from apps.authentication.schemas.login_schemas import LoginSchema

login_router = APIRouter()


@cbv(login_router)
class LoginViews:
    """Login views."""

    @login_router.post("/", response_model=dict)
    async def login(
        self,
        request: Request,
        credentials: OAuth2EmailPasswordRequestForm = Depends(
            OAuth2EmailPasswordRequestForm
        ),
    ):
        """Login endpoint."""
        login_schema = LoginSchema.model_validate({"email": credentials.username})
        client = request.headers.get("X-Client-ID", str(uuid.uuid4()))
        login_data = login_schema.login(credentials.password, client)
        return login_data
