from apps.authentication.methods.password_util_methods import (
    hash_password_with_secret_key,
    verify_password,
)
from fastapi__template.test import TestCase


class TestPasswordUtilMethods(TestCase):
    def setUp(self):
        super().setUp()
        self.password = "password"
        self.hashed_password = hash_password_with_secret_key(self.password)

    def test_hash_password_with_secret_key_returns_hashed_password(self):
        self.assertNotEqual(self.password, self.hashed_password)

    def test_verify_password_returns_true_for_valid_password(self):
        self.assertTrue(verify_password(self.hashed_password, self.password))

    def test_verify_password_returns_false_for_invalid_password(self):
        self.assertFalse(verify_password(self.hashed_password, "invalid_password"))
