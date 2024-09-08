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
from fastapi__template.dependencies import find_models
from fastapi__template.test.test_setup import engine


class TestCase(unittest.TestCase):
    """
    Base test case class.

    This class is intended to be used as a base class for all test cases.
    """

    def setUp(self):
        """Setup test environment."""
        self.app = app
        self.client = TestClient(self.app)
        self.base_model = SQLModel
        find_models()
        self.engine = engine
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
