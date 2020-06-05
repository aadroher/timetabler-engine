from tabulate import tabulate


def room_schedules(solution=None):
    curriculum_name = 'CiT'
    week_days = ['mon', 'tue', 'wed', 'thu', 'fri']
    time_slots = ['08', '09', '10', '11', '12', '13']

    headers = [curriculum_name] + week_days
    rows = [[time_slot] + [' '] * len(week_days)
            for time_slot in time_slots]
    return tabulate(rows, headers=headers)
