from collections import namedtuple
from itertools import product
from .loader import get_named_tuple

Session = namedtuple(
    'Session',
    [
        'room',
        'day',
        'time_slot',
        'teacher',
        'subject'
    ]
)


def from_data(rooms=[], days=[], time_slots=[], teachers=[], subjects=[]):
    return [
        Session(
            room=r,
            day=d,
            time_slot=h,
            teacher=t,
            subject=s
        ) for r, d, h, t, s in product(rooms, days, time_slots, teachers, subjects)
    ]
