"""Extension allowing to load other extensions using relative file paths."""

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

from copier.errors import UserMessageError
from jinja2 import environment as jinja_env_module
from jinja2.ext import Extension


class TemplateRelativePath(Extension):
    """Extension allowing to load other extensions using relative file paths."""

    def __init__(self, environment):
        """Initialize the object.

        Arguments:
            environment: The Jinja environment.
        """
        super().__init__(environment)
        # patch jinja's extension loading mechanism
        jinja_env_module.import_string = self._patched_import_string

    def _patched_import_string(self, import_name, silent=False):
        try:
            self._import_string(import_name)
        except Exception:
            if not silent:
                raise

    def _import_string(self, import_name):
        if ":" in import_name:
            module_name, obj = import_name.split(":", 1)
            module = self._import_module(module_name, try_filepath=True)

        elif "." in import_name:
            module_name, _, obj = import_name.rpartition(".")
            module = self._import_module(module_name)

        else:
            return __import__(import_name)

        return getattr(module, obj)

    def _import_module(self, name, try_filepath=False):
        try:
            return __import__(module_name, None, None, [obj])
        except ImportError:
            if try_filepath:
                return self._import_template_module(module_name)
            raise

    def _import_template_module(self, relative_path):
        module_name = Path(relative_path).stem
        for search_path in self.environment.loader.searchpath:  # noqa: WPS503
            template_relative_path = Path(search_path) / relative_path
            if template_relative_path.exists():
                break
        else:
            raise UserMessageError(
                f"Could not resolve path to local extension module '{relative_path}'\n"
                "Please report this issue to the template maintainers."
            )
        spec = spec_from_file_location(
            f"copier_templates_extensions.{module_name}",
            template_relative_path,
        )
        module = module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
