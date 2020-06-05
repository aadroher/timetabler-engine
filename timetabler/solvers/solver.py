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

    for r, d, h, t, s in sessions:
        if r.code != 'r01' or s.code in cit.subjects:
            model.Add(session_vars[(r, d, h, t, s)] == 1)
        if r.code != 'r02' or s.code in hcs.subjects:
            model.Add(session_vars[(r, d, h, t, s)] == 1)

    return model


def right_num_hours(model=None, session_vars={}, sessions=[]):
    cs = curricula.all()
    cit = next(c for c in cs if c.code == 'cit')
    hcs = next(c for c in cs if c.code == 'hcs')

    for curriculum in [cit, hcs]:
        common_subjects = curriculum.subjects[:4]
        modality_subjects = curriculum.subjects[4:]

        for common_subject in common_subjects:
            sessions_with_common_subjects = [
                (r, d, h, t, s) for r, d, h, t, s in sessions if s.code == common_subject
            ]
            model.Add(
                sum(session_vars[s] for s in sessions_with_common_subjects)
                == 3 * 2
            )

        for modality_subject in modality_subjects:
            sessions_with_modality_subjects = [
                (r, d, h, t, s) for r, d, h, t, s in sessions if s.code == modality_subject
            ]
            model.Add(
                sum(session_vars[s] for s in sessions_with_modality_subjects)
                == 4
            )

    return model


def solve():
    sessions = get_sessions()
    model, session_vars = get_session_vars(
        model=cp_model.CpModel(), sessions=sessions)

    model = separate_room_by_curriculum(
        model=model, session_vars=session_vars, sessions=sessions)
    model = right_num_hours(
        model=model, session_vars=session_vars, sessions=sessions)

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    pp('\n')
    # pp(solver.StatusName(status))
    # pp(session_vars[sessions[10]])
    pp(solver.ResponseStats())

    print(model.ModelStats())

    schedules = room_schedules(solver=solver, session_vars=session_vars)
    for schedule in schedules:
        print(schedule)
