"""

Base test class for all tests

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

import unittest

from fastapi__template.test_setup import TestSetup


class BaseTest(unittest.TestCase):
    """Base test class for all tests."""

    def setUp(self):
        """Set up test."""
        self.test_setup = TestSetup()
        self.app, self.db = next(self.test_setup.setup())

    def tearDown(self):
        """Tear down test."""
        self.test_setup.teardown()
