import importlib.util
from pathlib import Path
from jinja2.ext import Extension
from jinja2 import environment as jinja_env_module


def _import_template_module(relative_path):
    module_name = Path(relative_path).stem
    spec = importlib.util.spec_from_file_location(f"copier_templates_extensions.{module_name}", relative_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _special_import_string(import_name, silent=False):
    if ":" in import_name:
        module_name, obj = import_name.split(":", 1)
        try:
            module = __import__(module_name, None, None, [obj])
        except ImportError:
            try:
                module = _import_template_module(module_name)
            except Exception:
                if not silent:
                    raise

    elif "." in import_name:
        module_name, _, obj = import_name.rpartition(".")
        try:
            module = __import__(module_name, None, None, [obj])
        except ImportError:
            if not silent:
                raise

    else:
        try:
            return __import__(import_name)
        except ImportError:
            if not silent:
                raise

    try:
        return getattr(module, obj)
    except AttributeError:
        if not silent:
            raise


class SpecialExtension(Extension):
    """Jinja2 Extension to slugify string."""

    def __init__(self, environment):
        """Jinja2 Extension constructor."""
        super(SpecialExtension, self).__init__(environment)
        jinja_env_module.import_string = _special_import_string
