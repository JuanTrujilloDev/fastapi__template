from fastapi import HTTPException
from fastapi_sqlalchemy import db
from pydantic import (
    BaseModel,
    EmailStr,
    Field,
)

from apps.authentication.methods.token_util_methods import (
    create_access_token,
    create_refresh_token,
)
from apps.users.models.user import User
from apps.users.schemas.user_schemas import UserReadSchema


class LoginSchema(BaseModel):
    """Login schema."""

    email: EmailStr = Field(..., description="Email of the user")

    def validate_credentials(self, password: str):
        """Validate email and password."""
        user = db.session.query(User).filter_by(email=self.email).first()
        if not user or not user.validate_password(password):
            raise HTTPException(status_code=403, detail="Invalid credentials")

        return user

    def create_access_token(self, user: User, client: str):
        """Create access token."""
        return create_access_token(
            data={"sub": str(user.id), "email": user.email},
            user_id=user.id,
            client=client,
        )

    def create_refresh_token(self, user: User, client: str):
        """Create refresh token."""
        return create_refresh_token(
            data={"sub": str(user.id), "email": user.email},
            user_id=user.id,
            client=client,
        )

    def login(self, password: str, client: str):
        """Validate email and password."""
        user = self.validate_credentials(password)
        access_token = self.create_access_token(user, client)
        refresh_token = self.create_refresh_token(user, client)
        user_data = UserReadSchema.model_validate(user)
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": user_data,
        }
