from itertools import product
from ortools.sat.python.cp_model import CpSolverSolutionCallback
import tabulate as tabulate_module
from tabulate import tabulate
from ..models import rooms, days, time_slots, teachers, curricula, subjects
from ..models.sessions import Session

tabulate_module.PRESERVE_WHITESPACE = True


class SolutionPrinter(CpSolverSolutionCallback):
    def __init__(self, session_vars={}):
        CpSolverSolutionCallback.__init__(self)
        self.session_vars = session_vars
        self.solution_count = 0

    def get_row(self, room=None, time_slot=None):

        def get_day_sessions(day):
            return [
                Session(
                    room=room,
                    day=day,
                    time_slot=time_slot,
                    teacher=teacher,
                    curriculum=curriculum,
                    subject=subject
                ) for teacher, curriculum, subject in product(teachers.all(), curricula.all(), subjects.all())
            ]

        def exists(session):
            session_var = self.session_vars[session]
            return bool(self.BooleanValue(session_var))

        def get_slot_label(session_list):
            if len(session_list) == 0:
                return ' '
            else:
                return '|'.join([str(s) for s in session_list])

        time_slot_session_lists = [
            list(filter(exists, get_day_sessions(day)))
            for day in days.all()
        ]

        return [
            get_slot_label(session_list)
            for session_list in time_slot_session_lists
        ]

    def get_room_schedule(self, room=None):
        week_day_codes = [day.code for day in days.all()]
        headers = [room.code, *week_day_codes]
        rows = [
            [time_slot.code] +
            self.get_row(
                room=room,
                time_slot=time_slot
            )
            for time_slot in time_slots.all()
        ]
        return tabulate(rows, headers=headers)

    def room_schedules(self):
        return [
            self.get_room_schedule(room=room)
            for room in rooms.all()
        ]

    def OnSolutionCallback(self):
        self.solution_count += 1

        print('\n')
        print(f'SOLUTION: {self.solution_count}')
        print('\n')

        # print('\n')
        # print(self.solver.ResponseStats())
        # print('\n')
        # print(self.model.ModelStats())
        # print('\n\n')

        # if status == cp_model.UNFEASIBLE:
        #     print('UNFEASIBLE!')
        # else:
        # print(status)

        print('Group Schedules')
        print('===============')
        schedules = self.room_schedules()
        for schedule in schedules:
            print(schedule + '\n')
            print('-----------------')

        print('+++++++++++++++++++++++++++')
