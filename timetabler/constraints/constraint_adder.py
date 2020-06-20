from functools import reduce
from .mandatory import (
    distinct_subjects_per_slot_and_room,
    distinct_teachers_per_slot,
    hours_a_week_per_subject,
    subject_has_the_right_curriculum,
    has_the_right_teacher,
    room_curriculum_equivalence,
    min_hours,
    consecutive_sessions,
    max_subject_hours_per_day,
    same_teacher_for_subject_and_curriculum
)
from .desiderata import (
    minimize_teacher_work_days,
    minimize_teacher_sessions_deviation,
)


mandatory_constraints = [
    distinct_subjects_per_slot_and_room,
    distinct_teachers_per_slot,
    hours_a_week_per_subject,
    subject_has_the_right_curriculum,
    has_the_right_teacher,
    room_curriculum_equivalence,
    min_hours,
    consecutive_sessions,
    max_subject_hours_per_day,
    same_teacher_for_subject_and_curriculum
]

desiderata = [
    minimize_teacher_work_days,
    minimize_teacher_sessions_deviation
]


def add_constraints(model=None, session_vars={}, sessions=[]):
    return reduce(
        lambda updated_model, rule: rule(
            model=updated_model,
            session_vars=session_vars,
            sessions=sessions
        ),
        mandatory_constraints + desiderata,
        model
    )
