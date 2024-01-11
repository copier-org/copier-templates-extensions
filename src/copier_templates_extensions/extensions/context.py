"""Extension allowing to modify the Copier context."""

from __future__ import annotations

from typing import TYPE_CHECKING

from jinja2.ext import Extension

if TYPE_CHECKING:
    from jinja2 import Environment
from typing import Any, Callable, MutableMapping


class ContextHook(Extension):
    """Extension allowing to modify the Copier context."""

    update = True

    def __init__(extension_self: Extension, environment: Environment) -> None:  # noqa: N805
        """Initialize the object.

        Arguments:
            environment: The Jinja environment.
        """
        super().__init__(environment)  # type: ignore[misc]

        class ContextClass(environment.context_class):  # type: ignore[name-defined]
            def __init__(
                self,
                env: Environment,
                parent: dict[str, Any],
                name: str | None,
                blocks: dict[str, Callable],
                globals: MutableMapping[str, Any] | None = None,  # noqa: A002,ARG002
            ):
                if "_copier_conf" in parent:
                    if extension_self.update:  # type: ignore[attr-defined]
                        parent.update(extension_self.hook(parent))  # type: ignore[attr-defined]
                    else:
                        extension_self.hook(parent)  # type: ignore[attr-defined]
                super().__init__(env, parent, name, blocks)

        environment.context_class = ContextClass

    def hook(self, context: dict) -> dict:
        """Abstract hook. Does nothing.

        Override this method to either return
        a new context dictionary that will be used
        to update the original one,
        or modify the context object in-place.

        Arguments:
            context: The context to modify.

        Raises:
            NotImplementedError: This method must be overridden in a subclass,
                and instead return either the same context instance modified,
                or new context instance (dictionary).
        """
        raise NotImplementedError
