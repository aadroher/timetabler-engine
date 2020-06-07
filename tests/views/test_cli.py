from timetabler.views.cli import room_schedules


def test_room_schedules():
    table = room_schedules(None)
    print('\n'+table)
