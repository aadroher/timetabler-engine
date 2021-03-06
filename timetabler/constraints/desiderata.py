from itertools import product
from statistics import pstdev
from ..models import rooms, days, time_slots, teachers, curricula, subjects
from ..models.sessions import Session


def minimize_teacher_work_days(model=None, session_vars={}, sessions=[]):

    def day_activity(day=None, teacher=None):
        teacher_day_sessions = [
            session_vars[Session(r, day, h, teacher, c, s)]
            for r, h, c, s in product(rooms.all(), time_slots.all(), curricula.all(), subjects.all())
        ]
        return min(1, sum(teacher_day_sessions))

    num_work_days = sum([
        day_activity(day=d, teacher=t)
        for d, t in product(days.all(), teachers.all())
    ])

    model.Minimize(num_work_days)

    return model


# def minimize_teacher_sessions_deviation(model=None, session_vars={}, sessions=[]):
#     all_teachers = teachers.all()

#     def get_teacher_num_sessions(teacher=None):
#         return sum([
#             session_vars[Session(r, d, h, teacher, c, s)]
#             for r, d, h, c, s in product(
#                 rooms.all(),
#                 days.all(),
#                 time_slots.all(),
#                 curricula.all(),
#                 subjects.all()
#             )
#         ])

#     mean_teacher_sessions = sum([
#         get_teacher_num_sessions(teacher=t)
#         for t in all_teachers
#     ]) // len(all_teachers)

#     deviation = sum([
#         abs(get_teacher_num_sessions(teacher=t) - mean_teacher_sessions)
#         for t in all_teachers
#     ])

#     model.Minimize(deviation)

#     return model


def get_teacher_sessions_deviation(get_value=lambda x: x, session_vars={}):

    def get_teacher_num_sessions_week(teacher=None):
        return sum([
            get_value(
                session_vars[Session(r, d, h, teacher, c, s)]
            )
            for r, d, h, c, s in product(
                rooms.all(),
                days.all(),
                time_slots.all(),
                curricula.all(),
                subjects.all()
            )
        ])

    teacher_num_sessions_week = [
        get_teacher_num_sessions_week(teacher=t)
        for t in teachers.all()
    ]
    maximum = 30
    standard_deviation = pstdev(teacher_num_sessions_week)

    return ((maximum - standard_deviation) / maximum) * 100

    # max_standard_deviation =


def evaluate_solution(get_value=lambda x: x, session_vars={}):
    return sum([
        get_teacher_sessions_deviation(
            get_value=get_value, session_vars=session_vars
        )
    ])
