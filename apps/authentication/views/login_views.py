from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi_utils.cbv import cbv

from apps.authentication.schemas.login_schemas import LoginSchema

login_router = APIRouter()


@cbv(login_router)
class LoginViews:
    """Login views."""

    @login_router.post("/", response_model=dict)
    async def login(
        self, credentials: Annotated[HTTPBasicCredentials, Depends(HTTPBasic())]
    ):
        """Login endpoint."""
        login_schema = LoginSchema.model_validate({"email": credentials.username})
        login_data = login_schema.login(credentials.password)
        return login_data
