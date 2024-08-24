"""
Test setup file for the FastAPI project.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

from fastapi__template.app import app
from fastapi__template.settings import SETTINGS

engine_url = (
    f"postgresql://{SETTINGS.database_user}:{SETTINGS.database_password}"
    f"@{SETTINGS.database_host}:{SETTINGS.database_port}"
)
engine = sa.create_engine(engine_url)
test_db_name = SETTINGS.database_name + "_test"
with engine.connect() as connection:
    connection.execution_options(isolation_level="AUTOCOMMIT")
    exists = connection.execute(
        sa.text(f"SELECT 1 FROM pg_database WHERE datname = '{test_db_name}'")
    ).fetchone()
    if not exists:
        connection.execute(sa.text(f"CREATE DATABASE {test_db_name}"))

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class TestSetup:
    """Test setup class."""

    @staticmethod
    def setup():
        """Setup test environment."""
        try:
            db = TestingSessionLocal()
            SQLModel.metadata.create_all(bind=engine)
            yield app, db
        finally:
            SQLModel.metadata.drop_all(bind=engine)
            with engine.connect() as connection:
                connection.execution_options(isolation_level="AUTOCOMMIT")
                exists = connection.execute(
                    sa.text(f"SELECT 1 FROM pg_database WHERE datname = '{test_db_name}'")
                ).fetchone()
                if exists:
                    connection.execute(sa.text(f"DROP DATABASE {test_db_name}"))

    @staticmethod
    def teardown():
        """Teardown test environment."""
        pass
