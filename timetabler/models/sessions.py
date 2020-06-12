from collections import namedtuple
from itertools import product

SessionTuple = namedtuple(
    'SessionTuple',
    [
        'room',
        'day',
        'time_slot',
        'teacher',
        'curriculum',
        'subject',
    ]
)


class Session(SessionTuple):
    def __repr__(self):
        return ':'.join(item.code for item in self)


def from_data(rooms=[], days=[], time_slots=[], teachers=[], curricula=[], subjects=[]):
    return [
        Session(
            room=r,
            day=d,
            time_slot=h,
            teacher=t,
            curriculum=c,
            subject=s,
        )
        for r, d, h, t, c, s in product(rooms, days, time_slots, teachers, curricula, subjects)
    ]
