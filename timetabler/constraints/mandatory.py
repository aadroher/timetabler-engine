
from ..models.sessions import Session
from ..models import rooms, days, time_slots, teachers, subjects, curricula
from ..utils.printer import pp
from itertools import product, combinations


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


def subject_has_the_right_curriculum(model=None, session_vars={}, sessions=[]):
    for session in sessions:
        invalid_session = session.subject.code not in session.curriculum.subjects
        if invalid_session:
            model.Add(session_vars[session] == 0)

    return model


def has_the_right_teacher(model=None, session_vars={}, sessions=[]):
    for session in sessions:
        variable = session_vars[session]
        model.Add(
            variable <= int(session.subject.code in session.teacher.subjects)
        )

    return model


def room_curriculum_equivalence(model=None, session_vars={}, sessions=[]):
    cs = curricula.all()
    cit = next(c for c in cs if c.code == 'cit')
    hcs = next(c for c in cs if c.code == 'hcs')
    room_code_to_curriculum = {
        'r01': cit,
        'r02': hcs
    }

    for session in sessions:
        invalid_assignment = room_code_to_curriculum[session.room.code] != session.curriculum
        if invalid_assignment:
            model.Add(session_vars[session] == 0)

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


def max_subject_hours_per_day(model=None, session_vars={}, sessions=[]):
    for r, d, s in product(rooms.all(), days.all(), subjects.all()):
        room_day_subject_sessions = [
            session_vars[Session(r, d, h, t, c, s)]
            for h, t, c in product(time_slots.all(), teachers.all(), curricula.all())
        ]
        model.Add(sum(room_day_subject_sessions) <= 2)

    return model


def same_teacher_for_subject_and_curriculum(model=None, session_vars={}, sessions=[]):
    common_subjects_codes = [
        'cat', 'cas', 'ang', 'fil', 'cmc'
    ]

    def get_num_hours_week(subject):
        return 3 if subject.code in common_subjects_codes else 4

    for r, t, c, s in product(rooms.all(), teachers.all(), curricula.all(), subjects.all()):
        week_subject_teacher_sessions = [
            session_vars[Session(r, d, h, t, c, s)]
            for d, h in product(days.all(), time_slots.all())
        ]

        model.Add(sum(week_subject_teacher_sessions) <= get_num_hours_week(s))

        # model.AddLinearExpressionInDomain(sum(week_subject_teacher_sessions), [
        #                                   get_num_hours_week(s), 0])

        # num_sessions = len(week_subject_teacher_sessions)
        # index_combinations = combinations(
        #     range(0, num_sessions),
        #     get_num_hours_week(s)
        # )

        # def get_assignment(true_value_indexes):
        #     return tuple(
        #         1 if i in true_value_indexes else 0
        #         for i in range(0, num_sessions)
        #     )

        # allowed_assignments = [
        #     get_assignment(index_combination)
        #     for index_combination in index_combinations
        # ]

        # # print(len(allowed_assignments))

        # model.AddAllowedAssignments(
        #     week_subject_teacher_sessions,
        #     allowed_assignments
        # )

    return model
