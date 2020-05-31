from .loader import Loader


class Model:
    def __init__(self, collection_name, code):
        self.collection_name = collection_name
        self.code = code
        self.name = self.__record['name']

    @property
    def __record(self):
        return next(Loader(self.collection_name).by_code(self.code))
