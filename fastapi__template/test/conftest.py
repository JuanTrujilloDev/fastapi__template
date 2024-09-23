"""
Test setup file for the FastAPI project.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

from fastapi__template.test.test_setup import (
    TEST_DB_NAME,
    drop_test_database,
    prepare_test_database,
)


def pytest_collection_finish(session):
    """Prepare test database after collection finish."""
    print(f"\033[1mpreparing database: \033[0;0m{TEST_DB_NAME}")
    prepare_test_database()


def pytest_sessionfinish(session, exitstatus):
    """Drop test database after session finish."""
    print(f"\n\n\033[1mdropping database: \033[0;0m{TEST_DB_NAME}", end="")
    drop_test_database()
