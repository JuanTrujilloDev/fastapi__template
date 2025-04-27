from dataclasses import dataclass

from fastapi_sqlalchemy import db


@dataclass
class BaseView:
    model = None

    def get_queryset(self):
        """
        Get model queryset.
        """
        return db.session.query(self.model).filter_by(is_active=True)
