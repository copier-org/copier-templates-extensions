from __future__ import annotations
from dataclasses import dataclass
from jinja2.ext import Extension

@dataclass
class Test:
    key: str
    value: str

class Success(Extension):
    def __init__(self, environment):
        super().__init__(environment)
        environment.globals.update(success=True)
