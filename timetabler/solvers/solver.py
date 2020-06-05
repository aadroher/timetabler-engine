from itertools import product
from functools import reduce
from ortools.sat.python import cp_model
from ..utils.printer import pp
from ..models import rooms, days, time_slots, teachers, subjects, curricula
from ..views.cli import room_schedules


def get_session_codes(session):
    r, d, h, t, s = session
    return tuple(item.code for item in [r, d, h, t, s])


def get_sessions():
    rs = rooms.all()
    ds = days.all()
    hs = time_slots.all()
    ts = teachers.all()
    ss = subjects.all()

    combinations = product(rs, ds, hs, ts, ss)
    return list(combinations)


def get_session_vars(model=None, sessions=[]):

    def add_session_var(session_vars, session):
        codes = get_session_codes(session)
        var_name = '|'.join(codes)
        new_var = model.NewBoolVar(var_name)
        return {**session_vars, session: new_var}

    return (model, reduce(add_session_var, sessions, {}))

# Rules


def separate_room_by_curriculum(model=None, session_vars={}, sessions=[]):
    cs = curricula.all()
    cit = next(c for c in cs if c.code == 'cit')
    hcs = next(c for c in cs if c.code == 'hcs')

    for r, _, _, _, s in sessions:
        model.Add(r != 'r01' or s in cit.subjects)
        model.Add(r != 'r02' or s in hcs.subjects)

    return model


def solve():
    sessions = get_sessions()
    model, session_vars = get_session_vars(
        model=cp_model.CpModel(), sessions=sessions)

    model = separate_room_by_curriculum(
        model=model, session_vars=session_vars, sessions=sessions)

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    pp('\n')
    pp(solver.StatusName(status))
    pp(session_vars[sessions[10]])
    pp(solver.ResponseStats())

    print(model.ModelStats())

    schedules = room_schedules(solver=solver, session_vars=session_vars)
    for schedule in schedules:
        print(schedule)
