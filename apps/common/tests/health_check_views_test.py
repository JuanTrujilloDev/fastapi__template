from fastapi__template.test import TestCase


class TestHealthCheckViews(TestCase):
    """Test health check views."""

    def test_health_check_returns_200_status_code(self):
        """Test health check."""
        response = self.client.get("/health-check")
        assert response.status_code == 200

    def test_health_check_returns_json_response(self):
        """Test health check."""
        response = self.client.get("/health-check")
        assert response.json() == {"status": "ok"}
