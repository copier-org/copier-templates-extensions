from copier_templates_extensions import ContextHook


class ContextUpdater(ContextHook):
    update = False

    def hook(self, context):
        context["success"] = True
