from apps.authentication.methods.api_key_util_methods import (
    generate_api_key,
    hash_api_key,
    verify_api_key,
)
from fastapi__template.test import TestCase


class TestApiKeyUtilMethods(TestCase):
    def setUp(self):
        super().setUp()
        self.api_key = generate_api_key()
        self.hashed_api_key = hash_api_key(self.api_key)

    def test_generate_api_key_returns_api_key(self):
        self.assertTrue(generate_api_key())

    def test_hash_api_key_returns_hashed_api_key(self):
        self.assertNotEqual(self.api_key, self.hashed_api_key)

    def test_verify_api_key_returns_true_for_valid_api_key(self):
        self.assertTrue(verify_api_key(self.hashed_api_key, self.api_key))

    def test_verify_api_key_returns_false_for_invalid_api_key(self):
        self.assertFalse(verify_api_key(self.hashed_api_key, "invalid_api_key"))
