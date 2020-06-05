from itertools import product
from functools import reduce
from ortools.sat.python import cp_model
from ..utils.printer import pp
from ..models import rooms, days, time_slots, teachers, subjects


def get_session_vars():
    rs = rooms.all()
    ds = days.all()
    hs = time_slots.all()
    ts = teachers.all()
    ss = subjects.all()

    combinations = product(rs, ds, hs, ts, ss)
    combinations_list = list(combinations)

    # pp(len(combinations_list))
    # pp(combinations_list[:3])

    model = cp_model.CpModel()

    def reducer(session_vars, combination):
        pp(type(combination))
        r, d, h, t, s = combination
        var_name = '|'.join([item.code for item in [r, d, h, t, s]])
        new_var = model.NewBoolVar(var_name)

        pp(session_vars)
        pp(var_name)
        return {**session_vars, combination: new_var}

    return reduce(reducer, combinations_list, dict())


def solve():
    session_vars = get_session_vars()
    pp(session_vars)
