"""

User Model

This model is used to store the Users.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

from sqlmodel import Field

from apps.common.models.base_model import BaseModel


class User(BaseModel, table=True):
    """User model"""

    __tablename__ = "users"

    name: str = Field(..., description="Name of the user")
    email: str = Field(..., description="Email of the user")
    password: str = Field(..., description="Password of the user")
    is_superuser: bool = Field(default=False, description="Is user superuser")

    def __str__(self):
        return self.name
