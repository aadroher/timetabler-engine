from functools import reduce
from .mantadory import (
    has_the_right_teacher,
    distinct_subjects_per_slot_and_room,
    room_curriculum_equivalence,
    hours_a_week_per_subject
)


mandatory_constraints = [
    has_the_right_teacher,
    distinct_subjects_per_slot_and_room
    # hours_a_week_per_subject,
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
