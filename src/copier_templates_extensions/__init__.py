"""
Copier Templates Extensions package.

Special Jinja2 extension for Copier that allows to load extensions
using file paths relative to the template root instead of Python dotted paths.
"""

from typing import List

from copier_templates_extensions.extensions.context import ContextHook
from copier_templates_extensions.extensions.loader import TemplateExtensionLoader

__all__: List[str] = ["ContextHook", "TemplateExtensionLoader"]  # noqa: WPS410 (the only __variable__ we use)
