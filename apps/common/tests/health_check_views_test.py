"""

Test health check views

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

from fastapi.testclient import TestClient

from apps.common.tests.base_test import BaseTest


class TestHealthCheckViews(BaseTest):
    """Test health check views."""

    def test_health_check_returns_200_status_code(self):
        """Test health check."""
        response = TestClient(self.app).get("/health-check")
        assert response.status_code == 200

    def test_health_check_returns_json_response(self):
        """Test health check."""
        response = TestClient(self.app).get("/health-check")
        assert response.json() == {"status": "ok"}
