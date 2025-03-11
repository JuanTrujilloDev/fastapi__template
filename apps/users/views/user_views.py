"""

User Views

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

from uuid import UUID

from fastapi import APIRouter
from fastapi_sqlalchemy import db
from fastapi_utils.cbv import cbv

from apps.users.models.user import User
from apps.users.schemas.user_schemas import UserCreateSchema, UserReadSchema

user_router = APIRouter(tags=["User Actions"], prefix="/users")


@cbv(user_router)
class UserViews:
    """User views."""

    model = User

    def get_queryset(self):
        """
        Get User queryset.
        """
        return db.session.query(self.model).filter_by(is_active=True)

    @user_router.get("/", response_model=UserReadSchema)
    async def get_user(self, user_id: UUID):
        """Get a user."""
        user = self.get_queryset().filter_by(id=user_id).first()
        if not user:
            return {"error": "User not found"}

        return user

    @user_router.post("/", response_model=UserReadSchema)
    async def create_user(self, user_data: UserCreateSchema):
        """Create a user."""
        try:
            user = User(**user_data.model_dump())
            db.session.add(user)
            db.session.commit()
            return user
        except Exception as e:
            db.session.rollback()
            if "unique constraint" in str(e).lower() and "email" in str(e).lower():
                return {"error": "User with this email already exists"}
            raise
