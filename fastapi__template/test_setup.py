"""
Test setup file for the FastAPI project.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

import os

import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

from fastapi__template.app import app
from fastapi__template.database import get_engine
from fastapi__template.settings import SETTINGS

TEST_DB_NAME = SETTINGS.DATABASE_NAME + "_test"
EXISTS_COMMAND = {
    "postgresql": f"SELECT 1 FROM pg_database WHERE datname = '{TEST_DB_NAME}'",  # nosec: B608
    "mysql": (
        "SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA "  # nosec: B608
        f"WHERE SCHEMA_NAME = '{TEST_DB_NAME}'"  # nosec: B608
    ),
    "mssql": f"SELECT 1 FROM sys.databases WHERE name = '{TEST_DB_NAME}'",  # nosec: B608
    "postgresql+psycopg": f"SELECT 1 FROM pg_database WHERE datname = '{TEST_DB_NAME}'",  # nosec: B608
    "postgresql+psycopg2": f"SELECT 1 FROM pg_database WHERE datname = '{TEST_DB_NAME}'",  # nosec: B608
}
TEST_DB_ENGINE = get_engine(
    database_engine=SETTINGS.DATABASE_ENGINE_NAME,
    database_name=SETTINGS.DATABASE_NAME,
    database_user=SETTINGS.DATABASE_USER,
    database_password=SETTINGS.DATABASE_PASSWORD,
    database_host=SETTINGS.DATABASE_HOST,
    database_port=SETTINGS.DATABASE_PORT,
)


def prepare_test_database():
    """Prepare test database."""
    db_engine = sa.create_engine(TEST_DB_ENGINE)
    with db_engine.connect() as connection:
        connection.execution_options(isolation_level="AUTOCOMMIT")
        exists = connection.execute(
            sa.text(
                EXISTS_COMMAND[os.environ.get("DATABASE_ENGINE", "postgresql")].format(
                    database_name=TEST_DB_NAME
                )
            )
        ).fetchone()
        if not exists:
            connection.execute(sa.text(f"CREATE DATABASE {TEST_DB_NAME}"))
    return db_engine


engine = prepare_test_database()
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
                    sa.text(
                        EXISTS_COMMAND[
                            os.environ.get("DATABASE_ENGINE", "postgresql")
                        ].format(database_name=TEST_DB_NAME)
                    )
                ).fetchone()
                if exists:
                    connection.execute(sa.text(f"DROP DATABASE {TEST_DB_NAME}"))

    @staticmethod
    def teardown():
        """Teardown test environment."""
        pass
