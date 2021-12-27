"""Extension allowing to modify the Copier context."""

from jinja2.ext import Extension


class ContextHook(Extension):
    """Extension allowing to modify the Copier context."""

    update = True

    def __init__(extension_self, environment):  # noqa: N805 (self)
        """Initialize the object.

        Arguments:
            environment: The Jinja environment.
        """
        super().__init__(environment)

        class ContextClass(environment.context_class):  # noqa: WPS431 (nested class)
            def __init__(self, env, parent, name, blocks, globals=None):  # noqa: A002,VNE003
                if "_copier_conf" in parent:
                    if extension_self.update:
                        parent.update(extension_self.hook(parent))
                    else:
                        extension_self.hook(parent)
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
