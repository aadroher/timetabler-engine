from itertools import product
from functools import reduce
from ortools.sat.python import cp_model
from ..utils.printer import pp
from ..models import rooms, days, time_slots, teachers, subjects, curricula, sessions
from ..constraints.constraint_adder import add_constraints
from ..views.cli import room_schedules


def get_sessions():
    return sessions.from_data(
        rooms=rooms.all(),
        days=days.all(),
        time_slots=time_slots.all(),
        teachers=teachers.all(),
        subjects=subjects.all()
    )


def get_session_adder(model):
    def add_session_var(session_vars, session):
        var_name = '|'.join(item.code for item in session)
        new_var = model.NewBoolVar(var_name)
        return {**session_vars, session: new_var}
    return add_session_var


def get_session_vars(model=None, sessions=[]):
    return (model, reduce(get_session_adder(model), sessions, {}))


def solve():
    sessions = get_sessions()
    model, session_vars = get_session_vars(
        model=cp_model.CpModel(), sessions=sessions
    )
    constrained_model = add_constraints(
        model=model, session_vars=session_vars, sessions=sessions
    )

    solver = cp_model.CpSolver()
    solver.Solve(constrained_model)

    pp('\n')
    pp(solver.ResponseStats())

    print(model.ModelStats())

    schedules = room_schedules(solver=solver, session_vars=session_vars)
    for schedule in schedules:
        print(schedule + '\n')
