
from .loader import load_records

BATXILLERAT_CODE = 'bat'


def all():
    return load_records('Phase', 'phases')


def batxillerat():
    return next(p for p in all() if p.code == BATXILLERAT_CODE)


def curricula(phase=batxillerat()):
    curriculum_records = load_records('Curriculum', 'curricula')
