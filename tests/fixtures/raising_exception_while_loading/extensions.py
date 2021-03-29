from jinja2.ext import Extension


class HellRaiser(Extension):
    def __init__(self, environment):
        super().__init__(environment)
        raise RuntimeError("Hell raising!")
