from .loader import load_records


def all():
    return load_records('Curriculum', 'curricula')
