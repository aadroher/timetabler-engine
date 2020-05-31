
from amazing_printer import ap
from .loader import Loader
from .model import Model


class Phase(Model):
    def __init__(self, code):
        super().__init__('phases', code)

    @property
    def subjects(self):
        pass
