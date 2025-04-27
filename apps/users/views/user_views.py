"""

User Views

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

from uuid import UUID

from fastapi import APIRouter, Depends, status
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi_sqlalchemy import db
from fastapi_utils.cbv import cbv

from apps.authentication.permissions.base_permissions import (
    is_authenticated,
    is_superuser,
)
from apps.users.models.user import User
from apps.users.schemas.user_schemas import UserCreateSchema, UserReadSchema

user_router = APIRouter()


@cbv(user_router)
class UserViews:
    """User views."""

    model = User

    def get_queryset(self):
        """
        Get User queryset.
        """
        return db.session.query(self.model).filter_by(is_active=True)

    @user_router.get(
        "/",
        response_model=Page[UserReadSchema],
        dependencies=[
            Depends(is_authenticated),
            Depends(is_superuser),
        ],
    )
    async def get_users(self):
        """Get all users."""
        users = self.get_queryset().order_by(User.created_at)
        return paginate(users)

    @user_router.get(
        "/{user_id}}",
        response_model=UserReadSchema,
        status_code=status.HTTP_200_OK,
        dependencies=[
            Depends(is_authenticated),
            Depends(is_superuser),
        ],
    )
    async def get_user(self, user_id: UUID):
        """Get a user."""
        user = self.get_queryset().filter_by(id=user_id).first()
        if not user:
            return {"error": "User not found"}

        return user

    @user_router.post(
        "/", response_model=UserReadSchema, status_code=status.HTTP_201_CREATED
    )
    async def create_user(self, user_data: UserCreateSchema):
        """Create a user."""
        user = User(**user_data.model_dump())
        db.session.add(user)
        db.session.commit()
        return user
