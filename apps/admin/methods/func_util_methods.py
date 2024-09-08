import sqlalchemy as sa
from fastapi import FastAPI
from sqladmin import Admin

from apps.admin.admin import UserAdmin
from apps.authentication.admin import ApiKeyAdmin
from fastapi__template.settings import SETTINGS

engine = sa.create_engine(SETTINGS.DATABASE_ENGINE, poolclass=sa.StaticPool)


def register_admin_views(app: FastAPI):
    """Register admin views."""
    admin = Admin(app, engine)
    admin.add_view(UserAdmin)
    admin.add_view(ApiKeyAdmin)
