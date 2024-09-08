from sqlmodel import Field

from apps.common.models.base_model import BaseModel


class User(BaseModel, table=True):
    __tablename__ = "users"

    name: str = Field(..., description="Name of the user")
    email: str = Field(..., description="Email of the user")
    password: str = Field(..., description="Password of the user")
    is_superuser: bool = Field(default=False, description="Is user superuser")

    def __str__(self):
        return self.name
