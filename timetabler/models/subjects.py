from .loader import load_records


def subjects():
    return load_records('Subject', 'subjects')


def common_subjects():
    return [s for s in subjects() if s.type == 'com']


def modality_subjects():
    return [s for s in subjects() if s.type == 'mod']
