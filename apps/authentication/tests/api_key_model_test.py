import secrets
from datetime import datetime, timedelta
from unittest import mock

from pydantic_core import ValidationError

from apps.authentication.models.api_key import APIKey
from fastapi__template.test import TransactionTestCase


class TestApiKeyModel(TransactionTestCase):
    def setUp(self):
        super().setUp()
        self.secret_key = secrets.token_urlsafe(32)
        self.api_key = APIKey(
            title="test_key", description="Test Key", key=self.secret_key
        )
        self.past_date = datetime.now() - timedelta(days=1)
        with mock.patch(
            "apps.authentication.models.api_key.datetime"
        ) as mock_validate_expiry_date:
            mock_validate_expiry_date.now.return_value = datetime.now() - timedelta(
                days=2
            )
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

    def test_read_non_expired_api_key_with_is_active_false_is_enabled_return_false(self):
        api_key = self.db.session.query(APIKey).filter(APIKey.title == "test_key").first()
        api_key.is_active = False
        self.assertFalse(api_key.enabled)

    def test_create_api_key_returns_created_api_key(self):
        api_key = APIKey(
            title="new_key", description="New Key", key=secrets.token_urlsafe(32)
        )
        self.db.session.add(api_key)
        self.db.session.commit()
        self.assertEqual(api_key.title, "new_key")

    def test_update_api_key_returns_updated_api_key(self):
        api_key = self.db.session.query(APIKey).filter(APIKey.title == "test_key").first()
        api_key.title = "updated_key"
        self.db.session.commit()
        self.assertEqual(api_key.title, "updated_key")

    def test_delete_api_key_returns_deleted_api_key(self):
        api_key = self.db.session.query(APIKey).filter(APIKey.title == "test_key").first()
        self.db.session.delete(api_key)
        self.db.session.commit()
        self.assertIsNone(
            self.db.session.query(APIKey).filter(APIKey.title == "test_key").first()
        )

    def test_create_api_key_without_key_raises_error(self):
        with self.assertRaises(ValidationError) as e:
            APIKey(title="new_key", description="New Key")
        self.assertEqual(str(e.exception.errors()[0]["msg"]), "Field required")

    def test_create_api_key_with_non_string_key_raises_error(self):
        with self.assertRaises(ValueError) as e:
            APIKey(title="new_key", description="New Key", key=123)
        self.assertEqual(
            str(e.exception.errors()[0]["msg"]), "Input should be a valid string"
        )

    def test_create_api_key_with_past_expiry_date_raises_error(self):
        with self.assertRaises(ValueError) as e:
            APIKey(
                title="new_key",
                description="New Key",
                key=secrets.token_urlsafe(32),
                expiry_date=self.past_date,
            )
        self.assertEqual(
            str(e.exception.errors()[0]["msg"]),
            "Value error, Expiry date should be greater than today.",
        )

    def test_create_api_key_with_manual_key_returns_correct_short_key(self):
        api_key = APIKey(title="new_key32", description="New Key", key="testing key")
        self.db.session.add(api_key)
        self.db.session.commit()
        api_key = (
            self.db.session.query(APIKey).filter(APIKey.title == "new_key32").first()
        )
        self.assertEqual(api_key.short_key, "testi")
