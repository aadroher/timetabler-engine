from collections import namedtuple
from itertools import product
from .loader import get_named_tuple

SessionTuple = namedtuple(
    'SessionTuple',
    [
        'room',
        'day',
        'time_slot',
        'teacher',
        'subject'
    ]
)


class Session(SessionTuple):
    def __repr__(self):
        return ':'.join(item.code for item in self)


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
