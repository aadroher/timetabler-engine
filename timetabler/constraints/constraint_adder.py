from functools import reduce
from .mandatory import (
    has_the_right_teacher,
    distinct_subjects_per_slot_and_room,
    distinct_teachers_per_slot,
    room_curriculum_equivalence,
    hours_a_week_per_subject
)


mandatory_constraints = [
    # has_the_right_teacher,
    hours_a_week_per_subject,
    distinct_subjects_per_slot_and_room,
    distinct_teachers_per_slot
    # room_curriculum_equivalence,
]


def add_constraints(model=None, session_vars={}, sessions=[]):
    return reduce(
        lambda updated_model, rule: rule(
            model=updated_model,
            session_vars=session_vars,
            sessions=sessions
        ),
        mandatory_constraints,
        model
    )
