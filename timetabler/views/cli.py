from tabulate import tabulate
from ..models import rooms, days, time_slots, teachers, subjects


def get_slot_label(session):
    pass


def get_row(solver=None, session_vars={}, room=None, time_slot=None, days=days):
    ts = teachers.all()
    ss = subjects.all()

    row = []
    for day in days:
        slot_label_tokens = []
        for teacher in ts:
            for subject in ss:
                var_name = session_vars[
                    (room, day, time_slot, teacher, subject)
                ]
                # print(var_name)
                if solver.Value(var_name) == 1:
                    slot_label_tokens.extend(
                        [f'{teacher.code}:{subject.code}']
                    )
        slot_label = ' | '.join(slot_label_tokens[:3])
        row.append(slot_label)

    return row


def get_room_schedule(solver=None, session_vars={}, room=None):
    ds = days.all()
    week_day_codes = [day.code for day in ds]
    headers = [room.code] + week_day_codes
    rows = [
        [time_slot.code] +
        get_row(solver=solver, session_vars=session_vars,
                room=room, time_slot=time_slot, days=ds)
        for time_slot in time_slots.all()
    ]
    return tabulate(rows, headers=headers)


def room_schedules(solver=None, session_vars={}):
    return [get_room_schedule(solver=solver, session_vars=session_vars, room=room) for room in rooms.all()]
