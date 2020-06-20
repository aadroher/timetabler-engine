from itertools import product
from ortools.sat.python.cp_model import CpSolverSolutionCallback
import tabulate as tabulate_module
from tabulate import tabulate
from ..models import rooms, days, time_slots, teachers, curricula, subjects
from ..models.sessions import Session
from ..constraints.desiderata import evaluate_solution

tabulate_module.PRESERVE_WHITESPACE = True


class SolutionPrinter(CpSolverSolutionCallback):
    def __init__(self, session_vars={}):
        CpSolverSolutionCallback.__init__(self)
        self.session_vars = session_vars
        self.last_best_solution = {
            'solution': 0,
            'score': 0
        }
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

    def get_teacher_schedule_row(self, teacher=None, time_slot=None):
        def get_day_sessions(day):
            return [
                Session(
                    room=room,
                    day=day,
                    time_slot=time_slot,
                    teacher=teacher,
                    curriculum=curriculum,
                    subject=subject
                ) for room, curriculum, subject in product(rooms.all(), curricula.all(), subjects.all())
            ]

        def exists(session):
            session_var = self.session_vars[session]
            return bool(self.Value(session_var))

        def get_slot_label(session_list):
            if len(session_list) == 0:
                return ' ' * 18
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

    def get_teacher_schedule(self, solver=None, session_vars={}, teacher=None):
        week_day_codes = [day.code for day in days.all()]
        headers = [teacher.code, *week_day_codes]
        rows = [
            [time_slot.code] +
            self.get_teacher_schedule_row(
                teacher=teacher,
                time_slot=time_slot
            )
            for time_slot in time_slots.all()
        ]
        return tabulate(rows, headers=headers)

    def teacher_schedules(self, solver=None, session_vars={}):
        return [
            self.get_teacher_schedule(teacher=teacher)
            for teacher in teachers.all()
        ]

    def OnSolutionCallback(self):
        self.solution_count += 1
        new_solution_score = evaluate_solution(
            get_value=self.Value, session_vars=self.session_vars
        )
        if new_solution_score > self.last_best_solution['score']:
            self.last_best_solution = {
                'solution': self.solution_count,
                'score': new_solution_score
            }

            print('\n')
            print(f'NEW BEST SOLUTION!: {self.solution_count}')
            print(f'Score: {new_solution_score} %')
            print('\n')

            print('Group Schedules')
            print('===============')
            schedules = self.room_schedules()
            for schedule in schedules:
                print(schedule + '\n')
                print('-----------------')

            print('Teacher Schedules')
            print('=================')
            schedules = self.teacher_schedules()
            for schedule in schedules:
                print(schedule + '\n')
                print('\n')

            print('+++++++++++++++++++++++++++')
