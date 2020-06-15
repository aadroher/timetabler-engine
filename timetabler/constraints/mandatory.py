
from itertools import product
from ..utils.printer import pp
from ..models import rooms, days, time_slots, teachers, subjects, curricula
from ..models.sessions import Session


def has_the_right_teacher(model=None, session_vars={}, sessions=[]):
    for session in sessions:
        variable = session_vars[session]
        model.Add(
            variable <= int(session.subject.code in session.teacher.subjects)
        )

    return model


def distinct_subjects_per_slot_and_room(model=None, session_vars={}, sessions=[]):
    for r, d, h in product(rooms.all(), days.all(), time_slots.all()):
        subject_vars = [
            session_vars[Session(r, d, h, t, c, s)]
            for t, c, s in product(teachers.all(), curricula.all(), subjects.all())
        ]
        model.Add(sum(subject_vars) <= 1)

    return model


def distinct_teachers_per_slot(model=None, session_vars={}, sessions=[]):
    for d, h, t in product(days.all(), time_slots.all(), teachers.all()):
        teacher_vars = [
            session_vars[Session(r, d, h, t, c, s)]
            for r, c, s in product(rooms.all(), curricula.all(), subjects.all())
        ]
        model.Add(sum(teacher_vars) <= 1)

    return model


def room_curriculum_equivalence(model=None, session_vars={}, sessions=[]):
    # cs = curricula.all()
    # cit = next(c for c in cs if c.code == 'cit')
    # hcs = next(c for c in cs if c.code == 'hcs')
    # room_code_to_curriculum = {
    #     'r01': cit,
    #     'r02': hcs
    # }

    # for r, d, h, t, s in sessions:
    #     curriculum = room_code_to_curriculum[r.code]
    #     if s.code not in curriculum.subjects:
    #         model.Add(session_vars[(r, d, h, t, s)] == 0)

    without_curricula = product(
        rooms.all(),
        days.all(),
        time_slots.all(),
        teachers.all(),
        subjects.all()
    )

    for r, d, h, t, s in without_curricula:
        model.Add(
            sum(
                session_vars[Session(r, d, h, t, c, s)]
                for c in curricula.all()
            ) == 1
        )

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
                session for session in sessions
                if session.room.code == room_code and session.subject.code == subject_code
            ]
            subject_vars = [
                session_vars[s] for s in room_sessions_with_subject_code
            ]

            model.AddLinearConstraint(
                sum(subject_vars), hours_week, hours_week
            )

    return model


def min_hours(model=None, session_vars={}, sessions=[]):
    for r, d in product(rooms.all(), days.all()):
        room_day_vars = [
            session_vars[Session(r, d, h, t, c, s)]
            for h, t, c, s in product(time_slots.all(), teachers.all(), curricula.all(), subjects.all())
        ]
        model.Add(sum(room_day_vars) >= 5)

    return model


def consecutive_sessions(model=None, session_vars={}, sessions=[]):
    core_time_slots = [
        h for h in time_slots.all() if h.position in range(1, 5)
    ]
    for r, d in product(rooms.all(), days.all()):
        core_time_slot_vars = [
            session_vars[Session(r, d, h, t, c, s)]
            for h, t, c, s in product(core_time_slots, teachers.all(), curricula.all(), subjects.all())
        ]
        model.Add(sum(core_time_slot_vars) == 4)

    return model
