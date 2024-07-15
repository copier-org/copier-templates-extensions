"""Extension allowing to modify the Copier context."""

from __future__ import annotations

import warnings
from typing import TYPE_CHECKING

from jinja2.ext import Extension

if TYPE_CHECKING:
    from collections.abc import Callable, MutableMapping

    from jinja2 import Environment

_sentinel = object()


class ContextHook(Extension):
    """Extension allowing to modify the Copier context."""

    update = _sentinel

    def __init__(extension_self, environment: Environment) -> None:  # noqa: N805
        """Initialize the object.

        Arguments:
            environment: The Jinja environment.
        """
        super().__init__(environment)

        class ContextClass(environment.context_class):  # type: ignore[misc,name-defined]
            def __init__(
                self,
                env: Environment,
                parent: dict[str, Any],
                name: str | None,
                blocks: dict[str, Callable[..., Any]],
                globals: MutableMapping[str, Any] | None = None,  # noqa: A002,ARG002
            ):
                if extension_self.update is not _sentinel:  # type: ignore[attr-defined]
                    warnings.warn(
                        "The `update` attribute of `ContextHook` subclasses is deprecated. "
                        "The `hook` method should now always modify the `context` in place.",
                        DeprecationWarning,
                        stacklevel=1,
                    )
                if "_copier_conf" in parent and (context := extension_self.hook(parent)) is not None:  # type: ignore[attr-defined]
                    parent.update(context)
                    warnings.warn(
                        "Returning a dict from the `hook` method is deprecated. "
                        "It should now always modify the `context` in place.",
                        DeprecationWarning,
                        stacklevel=1,
                    )
                super().__init__(env, parent, name, blocks)

        environment.context_class = ContextClass

    def hook(self, context: dict[str, Any]) -> dict[str, Any]:
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
