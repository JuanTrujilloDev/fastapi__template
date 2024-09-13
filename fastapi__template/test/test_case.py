"""
Test setup file for the FastAPI project.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

import unittest
from unittest.mock import Mock

from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

from fastapi__template.app import app
from fastapi__template.dependencies import DEFAULT_ENGINE, find_models


class TestCase(unittest.TestCase):
    """
    Base test case.
    This test can be used for tests that do not require a database connection.
    """

    def setUp(self):
        """Setup test environment."""
        self.app = app
        self.client = TestClient(self.app)

    def tearDown(self):
        """Teardown test environment."""
        pass


class TransactionTestCase(unittest.TestCase):
    """
    Transactional test case.
    This test can be used for tests that require a database connection.
    """

    def setUp(self):
        """Setup test environment."""
        self.app = app
        self.client = TestClient(self.app)
        self.base_model = SQLModel
        find_models()
        self.engine = DEFAULT_ENGINE
        self.session = sessionmaker(bind=self.engine)()
        self.db = Mock()
        self.db.session = self.session
        with self.engine.begin() as connection:
            self.base_model.metadata.drop_all(connection)
            self.base_model.metadata.create_all(connection)
            connection.commit()
            connection.close()

    def tearDown(self):
        """Teardown test environment."""
        with self.engine.begin() as connection:
            self.base_model.metadata.drop_all(connection)
            self.base_model.metadata.create_all(connection)
            connection.commit()
            connection.close()
