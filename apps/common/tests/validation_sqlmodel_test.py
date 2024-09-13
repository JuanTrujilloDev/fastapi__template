from apps.common.models.validation_sqlmodel import ValidationSQLModelMeta
from fastapi__template.test import TestCase


class ValidationSQLModelTest(TestCase):
    """Base model test case."""

    def test_class_without_model_config_raises_exception(self):
        """Test base model."""
        with self.assertRaises(AttributeError) as e:

            class ModelWithoutModelConfig(metaclass=ValidationSQLModelMeta):
                pass

        self.assertEqual(
            str(e.exception),
            "model_config",
        )

    def test_class_with_model_config_raises_no_exception(self):
        """Test base model."""

        class ModelWithModelConfig(metaclass=ValidationSQLModelMeta):
            model_config = {}

        ModelWithModelConfig()
        self.assertIsInstance(ModelWithModelConfig, ValidationSQLModelMeta)
