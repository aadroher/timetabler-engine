
from amazing_printer import ap
from .loader import Loader


class Phase:
    def __init__(self, code):
        self.code = code

    @property
    def __record(self):
        return next(Loader('phases').by_code(self.code))

    @property
    def name(self):
        return self.__record['name']
