import bcrypt

from apps.authentication.methods.hash_util_methods import (
    hash_string_with_secret_key,
    verify_strings,
)
from fastapi__template.test import TestCase


class TestPasswordUtilMethods(TestCase):
    def setUp(self):
        super().setUp()
        self.password = "password"
        self.salt = bcrypt.gensalt()
        self.hashed_password = hash_string_with_secret_key(self.password, self.salt)

    def test_when_hash_string_with_then_secret_key_returns_hashed_string(self):
        self.assertNotEqual(self.password, self.hashed_password)

    def test_when_verify_string_then_returns_true_for_valid_string(self):
        self.assertTrue(verify_strings(self.hashed_password, self.salt, self.password))

    def test_when_verify_string_then_returns_false_for_invalid_string(self):
        self.assertFalse(
            verify_strings(self.hashed_password, self.salt, "invalid_password")
        )
