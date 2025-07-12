from copier_template_extensions import ContextHook


class ContextUpdater(ContextHook):
    update = "not sentinel"

    def hook(self, context):
        context["success"] = True
