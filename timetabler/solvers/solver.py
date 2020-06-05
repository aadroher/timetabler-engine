from itertools import product
from functools import reduce
from ortools.sat.python import cp_model
from ..utils.printer import pp
from ..models import rooms, days, time_slots, teachers, subjects, curricula


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
        r, d, h, t, s = session
        codes = tuple(item.code for item in [r, d, h, t, s])
        var_name = '|'.join(codes)
        new_var = model.NewBoolVar(var_name)
        return {**session_vars, codes: new_var}

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

    print(model.ModelStats())
