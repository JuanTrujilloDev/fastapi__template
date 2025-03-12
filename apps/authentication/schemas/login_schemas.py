from fastapi import HTTPException
from fastapi_sqlalchemy import db
from pydantic import BaseModel, ConfigDict, EmailStr, Field, model_validator

from apps.authentication.methods.hash_util_methods import verify_strings
from apps.users.models.user import User


class LoginSchema(BaseModel):
    """Login schema."""

    email: EmailStr = Field(..., description="Email of the user")
    password: str = Field(..., description="Password of the user")

    model_config = ConfigDict(from_attributes=True, extra="allow")

    @model_validator(mode="after")
    def validate_credentials(self):
        """Validate email and password."""
        user = db.session.query(User).filter_by(email=self.email).first()
        if not user or not verify_strings(user.password, self.password):
            raise HTTPException(status_code=403, detail="Invalid credentials")

        self.user = user
        return self

    def login(self):
        """Login user."""
        # TODO: Implement login logic
        return {"status": "ok"}
