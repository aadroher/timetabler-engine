from .utils.printer import pp
from .models.loader import load_records


bat_code = 'bat'


def get_batxillerat():
    phases = load_records(type_name='Phase', collection_name='phases')
    return next(p for p in phases if p.code == bat_code)


def main():
    batxillerat = get_batxillerat()
    pp(batxillerat)
