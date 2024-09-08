"""

Metaclass for SQLModel validation

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

from sqlmodel.main import SQLModelMetaclass


class ValidationSQLModelMeta(SQLModelMetaclass):
    """Metaclass for SQLModel validation"""

    def __call__(cls, *args, **kwargs):
        """Call method for SQLModel validation"""
        if not hasattr(cls, "model_config"):
            raise ValueError("model_config is not defined in the model.")

        cls.model_config["table"] = False
        model = super().__call__(*args, **kwargs)
        cls.model_config["table"] = True
        return model
