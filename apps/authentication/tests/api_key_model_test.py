import secrets
from datetime import datetime, timedelta

from apps.authentication.models.api_key import APIKey
from fastapi__template.test import TestCase


class TestApiKeyModel(TestCase):
    def setUp(self):
        super().setUp()
        self.api_key = APIKey(
            title="test_key", description="Test Key", key=secrets.token_urlsafe(32)
        )
        self.past_date = datetime.now() - timedelta(days=1)
        self.expired_api_key = APIKey(
            title="expired_key",
            description="Expired Key",
            expiry_date=self.past_date,
            key=secrets.token_urlsafe(32),
        )
        self.db.session.add_all([self.api_key, self.expired_api_key])
        self.db.session.commit()

    def test_read_api_key_returns_correct_api_key(self):
        api_key = self.db.session.query(APIKey).filter(APIKey.title == "test_key").first()
        self.assertEqual(api_key.title, "test_key")

    def test_read_expired_api_key_is_enabled_return_false(self):
        api_key = (
            self.db.session.query(APIKey).filter(APIKey.title == "expired_key").first()
        )
        self.assertFalse(api_key.enabled)

    def test_read_non_expired_api_key_is_enabled_return_true(self):
        api_key = self.db.session.query(APIKey).filter(APIKey.title == "test_key").first()
        self.assertTrue(api_key.enabled)
