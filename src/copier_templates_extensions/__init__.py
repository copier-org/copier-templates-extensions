"""Deprecated. Import from `copier-template-extensions` instead."""

# YORE: Bump 1: Remove file.

import warnings

from copier_template_extensions import ContextHook, TemplateExtensionLoader

__all__: list[str] = ["ContextHook", "TemplateExtensionLoader"]

warnings.warn(
    "`copier-templates-extensions` is renamed `copier-template-extensions`. "
    "Please use the new name, and replace every occurrence of "
    "`copier-templates-extensions` and `copier_templates_extensions` in your template with "
    "`copier-template-extensions` and `copier_template_extensions` respectively.",
    DeprecationWarning,
    stacklevel=2,
)
