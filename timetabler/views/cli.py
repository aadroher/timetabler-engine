from itertools import product
from tabulate import tabulate
from ..models import rooms, days, time_slots, teachers, subjects
from ..models.sessions import Session


def get_row(solver=None, session_vars={}, room=None, time_slot=None):
    def get_day_sessions(day):
        return [
            Session(
                room=room,
                day=day,
                time_slot=time_slot,
                teacher=teacher,
                subject=subject
            ) for teacher, subject in product(teachers.all(), subjects.all())
        ]

    def exists(session):
        session_var = session_vars[session]
        return bool(solver.Value(session_var))

    def get_slot_label(session_list):
        if len(session_list) == 0:
            return ' '
        else:
            return str(session_list[0])

    time_slot_session_lists = [
        list(filter(exists, get_day_sessions(day)))
        for day in days.all()
    ]

    return [
        get_slot_label(session_list)
        for session_list in time_slot_session_lists
    ]


def get_room_schedule(solver=None, session_vars={}, room=None):
    ds = days.all()
    week_day_codes = [day.code for day in ds]
    headers = [room.code] + week_day_codes
    rows = [
        [time_slot.code] +
        get_row(
            solver=solver,
            session_vars=session_vars,
            room=room,
            time_slot=time_slot
        )
        for time_slot in time_slots.all()
    ]
    return tabulate(rows, headers=headers)


def room_schedules(solver=None, session_vars={}):
    return [get_room_schedule(solver=solver, session_vars=session_vars, room=room) for room in rooms.all()]
