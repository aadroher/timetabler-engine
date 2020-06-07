
from itertools import product
from ..utils.printer import pp
from ..models import rooms, days, time_slots, teachers, subjects, curricula


def has_the_right_teacher(model=None, session_vars={}, sessions=[]):
    for r, d, h, t, s in sessions:
        variable = session_vars[(r, d, h, t, s)]
        model.Add(variable == int(s.code in t.subjects))

    return model


def distinct_subjects_per_slot_and_room(model=None, session_vars={}, sessions=[]):
    ss = subjects.all()
    for r, d, h, t in product(rooms.all(), days.all(), time_slots.all(), teachers.all()):
        subject_vars = [
            session_vars[(r, d, h, t, s)]
            for s in ss
        ]
        model.AddLinearConstraint(sum(subject_vars), 0, 1)

    return model


def distinct_teachers_per_slot_and_room(model=None, session_vars={}, sessions=[]):
    ts = teachers.all()
    for r, d, h, t in product(rooms.all(), days.all(), time_slots.all(), teachers.all()):
        teacher_vars = [
            session_vars[(r, d, h, t, s)]
            for s in ts
        ]
        model.Add(sum(teacher_vars) <= 1)

    return model


def room_curriculum_equivalence(model=None, session_vars={}, sessions=[]):
    cs = curricula.all()
    cit = next(c for c in cs if c.code == 'cit')
    hcs = next(c for c in cs if c.code == 'hcs')

    for r, d, h, t, s in sessions:
        if r.code != 'r01' or s.code in cit.subjects:
            model.Add(session_vars[(r, d, h, t, s)] == 1)
        if r.code != 'r02' or s.code in hcs.subjects:
            model.Add(session_vars[(r, d, h, t, s)] == 1)

    return model


def hours_a_week_per_subject(model=None, session_vars={}, sessions=[]):
    for curriculum in curricula.all():
        common_subject_codes = curriculum.subjects[:5]
        modality_subject_codes = curriculum.subjects[5:]
        sujects_codes_and_hours = [
            (subject_code, 3) for subject_code in common_subject_codes
        ] + [
            (subject_code, 4) for subject_code in modality_subject_codes
        ]

        for subject_code, hours_week in sujects_codes_and_hours:
            room_code = {'cit': 'r01', 'hcs': 'r02'}[curriculum.code]
            room_sessions_with_subject_code = [
                (r, d, h, t, s) for r, d, h, t, s in sessions
                if r.code == room_code and s.code == subject_code
            ]
            subject_vars = [
                session_vars[s] for s in room_sessions_with_subject_code
            ]

            model.AddLinearConstraint(
                sum(subject_vars), hours_week, hours_week
            )

    return model
