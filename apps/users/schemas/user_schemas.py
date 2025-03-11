from pydantic import BaseModel, ConfigDict, EmailStr, Field

from apps.common.schemas.base_model_schema import BaseModelSchema


class UserCreateSchema(BaseModel):
    """User create schema."""

    email: EmailStr
    first_name: str
    last_name: str
    password: str

    model_config = ConfigDict(from_attributes=True)


class UserReadSchema(UserCreateSchema, BaseModelSchema):
    """User schema."""

    password: None = Field(None, exclude=True)

    model_config = ConfigDict(from_attributes=True)
