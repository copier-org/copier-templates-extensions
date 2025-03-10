"""Copier Templates Extensions package.

Special Jinja2 extension for Copier that allows to load extensions
using file paths relative to the template root instead of Python dotted paths.
"""

from __future__ import annotations

from copier_templates_extensions._internal.context import ContextHook
from copier_templates_extensions._internal.loader import TemplateExtensionLoader

__all__: list[str] = ["ContextHook", "TemplateExtensionLoader"]
