from .loader import load_records


def all():
    return load_records('Subject', 'subjects')


def common():
    return [s for s in all() if s.type == 'com']


def modality():
    return [s for s in all() if s.type == 'mod']
