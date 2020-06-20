from itertools import product
from functools import reduce
from ortools.sat.python import cp_model
from ..utils.printer import pp
from ..models import rooms, days, time_slots, teachers, subjects, curricula, sessions
from ..constraints.constraint_adder import add_constraints
from ..views.cli import room_schedules, teacher_schedules
from ..views.solution_printer import SolutionPrinter


def get_sessions():
    return sessions.from_data(
        rooms=rooms.all(),
        days=days.all(),
        time_slots=time_slots.all(),
        teachers=teachers.all(),
        curricula=curricula.all(),
        subjects=subjects.all()
    )


def get_session_adder(model):
    def add_session_var(session_vars, session):
        var_name = ':'.join(item.code for item in session)
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
    solution_printer = SolutionPrinter(session_vars=session_vars)
    solver.SolveWithSolutionCallback(constrained_model, solution_printer)

    print('\n')
    print(solver.ResponseStats())
    print('\n')
    print(model.ModelStats())
    print('\n\n')

    # if status == cp_model.UNFEASIBLE:
    #     print('UNFEASIBLE!')
    # else:
    # print(status)

    # print('Group Schedules')
    # print('===============')
    # schedules = room_schedules(solver=solver, session_vars=session_vars)
    # for schedule in schedules:
    #     print(schedule + '\n')
    #     print('-----------------')

    # print('Teacher Schedules')
    # print('=================')
    # schedules = teacher_schedules(solver=solver, session_vars=session_vars)
    # for schedule in schedules:
    #     print(schedule + '\n')
    #     print('\n')
