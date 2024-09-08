from apps.common.models.base_model import BaseModel
from fastapi__template.test import TestCase


class BaseModelTest(TestCase):
    """Base model test case."""

    def test_base_model_has_desired_attributes(self):
        """Test base model."""
        base_model = BaseModel()
        desired_attributes = [
            "id",
            "created_at",
            "updated_at",
            "is_active",
        ]
        self.assertTrue(
            all(hasattr(base_model, attribute) for attribute in desired_attributes)
        )
