"""
Copier Templates Extensions package.

Special Jinja2 extension for Copier that allows to load extensions using file paths relative to the template root instead of Python dotted paths.
"""

from typing import List

from copier_templates_extensions._extension import SpecialExtension as Ext

__all__: List[str] = ["Ext"]  # noqa: WPS410 (the only __variable__ we use)
