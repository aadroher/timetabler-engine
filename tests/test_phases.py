from timetabler.models import phases
from timetabler.utils.printer import pp


def test_phases():
    batxillerat = phases.batxillerat()
    pp(batxillerat)


def test_curricula():
    curricula = phases.curricula()
    pp(curricula)
