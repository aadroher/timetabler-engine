
from itertools import product
from ..utils.printer import pp
from ..models import rooms, days, time_slots, teachers, subjects, curricula


def has_the_right_teacher(model=None, session_vars={}, sessions=[]):
    for r, d, h, t, s in sessions:
        variable = session_vars[(r, d, h, t, s)]
        model.Add(variable == int(s.code in t.subjects))

    return model


def distinct_subjects_per_slot_and_room(model=None, session_vars={}, sessions=[]):
    ss = subjects.all()
    for r, d, h, t in product(rooms.all(), days.all(), time_slots.all(), teachers.all()):
        subject_vars = [
            session_vars[(r, d, h, t, s)]
            for s in ss
        ]
        model.Add(sum(subject_vars) <= 1)

    return model


def room_curriculum_equivalence(model=None, session_vars={}, sessions=[]):
    cs = curricula.all()
    cit = next(c for c in cs if c.code == 'cit')
    hcs = next(c for c in cs if c.code == 'hcs')

    for r, d, h, t, s in sessions:
        if r.code != 'r01' or s.code in cit.subjects:
            model.Add(session_vars[(r, d, h, t, s)] == 1)
        if r.code != 'r02' or s.code in hcs.subjects:
            model.Add(session_vars[(r, d, h, t, s)] == 1)

    return model


def hours_a_week_per_subject(model=None, session_vars={}, sessions=[]):
    cs = curricula.all()
    cit = next(c for c in cs if c.code == 'cit')
    hcs = next(c for c in cs if c.code == 'hcs')

    for curriculum in [cit, hcs]:
        common_subjects = curriculum.subjects[:4]
        modality_subjects = curriculum.subjects[4:]

        pp(common_subjects)
        for common_subject in common_subjects:
            room_code = {'cit': 'r01', 'hcs': 'r02'}[curriculum.code]
            pp(common_subject)
            sessions_with_common_subject = [
                (r, d, h, t, s) for r, d, h, t, s in sessions
                if r.code == room_code and s.code == common_subject
            ]
            pp(sessions_with_common_subject)
            common_subject_vars = [
                session_vars[s] for s in sessions_with_common_subject
            ]
            # pp(common_subjects_vars)
            model.Add(sum(common_subject_vars) == 3)

        # for modality_subject in modality_subjects:
        #     sessions_with_modality_subjects = [
        #         (r, d, h, t, s) for r, d, h, t, s in sessions if s.code == modality_subject
        #     ]
        #     model.Add(
        #         sum(session_vars[s] for s in sessions_with_modality_subjects)
        #         == 4
        #     )

    return model
