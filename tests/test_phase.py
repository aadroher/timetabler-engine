
from amazing_printer import ap
from timetabler.models.phase import Phase

BAT_CODE = 'bat'


def test_phase():
    phase = Phase(BAT_CODE)
    ap(phase)
    ap(phase.name)
    ap(phase.subjects)
