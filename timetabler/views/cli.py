from itertools import product
import tabulate as tabulate_module
from tabulate import tabulate
from ..models import rooms, days, time_slots, teachers, curricula, subjects
from ..models.sessions import Session

tabulate_module.PRESERVE_WHITESPACE = True


def get_row(solver=None, session_vars={}, room=None, time_slot=None):
    def get_day_sessions(day):
        return [
            Session(
                room=room,
                day=day,
                time_slot=time_slot,
                teacher=teacher,
                curriculum=curriculum,
                subject=subject
            ) for teacher, curriculum, subject in product(teachers.all(), curricula.all(), subjects.all())
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
    week_day_codes = [day.code for day in days.all()]
    headers = [room.code, *week_day_codes]
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
    return [
        get_room_schedule(solver=solver, session_vars=session_vars, room=room)
        for room in rooms.all()
    ]


def get_teacher_schedule_row(solver=None, session_vars={}, teacher=None, time_slot=None):
    def get_day_sessions(day):
        return [
            Session(
                room=room,
                day=day,
                time_slot=time_slot,
                teacher=teacher,
                curriculum=curriculum,
                subject=subject
            ) for room, curriculum, subject in product(rooms.all(), curricula.all(), subjects.all())
        ]

    def exists(session):
        session_var = session_vars[session]
        return bool(solver.Value(session_var))

    def get_slot_label(session_list):
        if len(session_list) == 0:
            return ' ' * 18
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


def get_teacher_schedule(solver=None, session_vars={}, teacher=None):
    week_day_codes = [day.code for day in days.all()]
    headers = [teacher.code, *week_day_codes]
    rows = [
        [time_slot.code] +
        get_teacher_schedule_row(
            solver=solver,
            session_vars=session_vars,
            teacher=teacher,
            time_slot=time_slot
        )
        for time_slot in time_slots.all()
    ]
    return tabulate(rows, headers=headers)


def teacher_schedules(solver=None, session_vars={}):
    return [
        get_teacher_schedule(
            solver=solver, session_vars=session_vars, teacher=teacher
        )
        for teacher in teachers.all()
    ]
