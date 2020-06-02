from itertools import product
from ortools.sat.python import cp_model
from ..utils.printer import pp
from ..models import rooms, days, time_slots, teachers, subjects


def solve():
    rs = rooms.all()
    ds = days.all()
    hs = time_slots.all()
    ts = teachers.all()
    ss = subjects.all()

    combinations = product(rs, ds, hs, ts, ss)
    combinations_list = list(combinations)

    model = cp_model.CpModel()

    for r, d, h, t, s in combinations_list:
        var_name = '|'.join([item.code for item in [r, d, h, t, s]])

    pp(len(combinations_list))
    pp(combinations_list[:3])
