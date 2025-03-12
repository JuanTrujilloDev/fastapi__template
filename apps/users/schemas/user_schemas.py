from pydantic import BaseModel, ConfigDict, EmailStr

from apps.common.schemas.base_model_schema import BaseModelSchema


class UserCreateSchema(BaseModel):
    """User create schema."""

    email: EmailStr
    first_name: str
    last_name: str
    password: str

    model_config = ConfigDict(from_attributes=True)


class UserReadSchema(BaseModelSchema):
    """User schema."""

    email: EmailStr
    first_name: str
    last_name: str

    model_config = ConfigDict(from_attributes=True)
