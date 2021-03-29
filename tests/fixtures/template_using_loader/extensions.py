from jinja2.ext import Extension


class Success(Extension):
    def __init__(self, environment):
        super().__init__(environment)
        environment.globals.update(success=True)
