"""

Admin site module

This file is used to register the admin views.

This file is subject to the terms and conditions defined in file 'LICENSE',
which is part of this source code package.
"""

from importlib import import_module

from sqladmin import Admin

from fastapi__template.admin.base_admin_views import BaseAdminView, BaseModelAdminView


def register(site=None):
    """Register admin views."""

    def _model_admin_wrapper(admin_class):
        app_module = import_module("fastapi__template.app")
        app = app_module.app
        admin_site = site or app.default_admin
        if not isinstance(admin_site, Admin):
            raise ValueError("site must subclass sqladmin.Admin class")

        if not issubclass(admin_class, (BaseModelAdminView, BaseAdminView)):
            raise ValueError(
                "Wrapped class must subclass BaseModelAdminView or BaseAdminView."
            )

        admin_site.add_view(admin_class)

        return admin_class

    return _model_admin_wrapper
