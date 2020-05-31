from amazing_printer import ap
from .loader import Loader
from .model import Model


class Subject(Model):
    def __init__(self, code):
        super().__init__('subjects', code)
