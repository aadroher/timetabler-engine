from .loader import load_records, get_named_tuple


def per_subject():
    subjects = load_records('Subject', 'subjects')
    return [
        get_named_tuple('Teacher', {
            'name': f'Teacher {i}',
            'code': subject.code,
            'subjects': (subject.code, )
        })
        for i, subject in enumerate(subjects)
    ]


def all():
    return load_records('Teacher', 'teachers')
    # return per_subject()
