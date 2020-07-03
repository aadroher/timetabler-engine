# Timetabler Engine

(_Alright, the name is not the most imaginative one, it may eventually get better_)

## What 

This is the result of my first attempts at discovering the possibilities of [Constraint Satisfaction Problem (CPS)](https://en.wikipedia.org/wiki/Constraint_satisfaction_problem) solvers, in particular of [Boolean Satisfiability Problems (SAT)](https://en.wikipedia.org/wiki/Boolean_satisfiability_problem).

This is a proof of concept that takes a toy example of a high school and tries to generate a session schedule for it by finding possible assignments of classroom / groups, teachers and subjects to time slots in week days. It uses the CP-SAT solver of [Google's OR-Tools](https://developers.google.com/optimization/cp/cp_solver)

### Installation

This project uses [Poetry](https://python-poetry.org/). Therefore, it's just a matter of installing it and
run:

```
$ poetry install
```

### Data
The data that represents the high school toy example lies as YAML files under `/data`

### Variables
The problem is approached by considering as variables all the possible sessions, which are represented as combinations of

```
session = { room, day, time_slot, teacher, curriculum, subject }
```

The session is added to the schedule if an only if `session == 1`. 

The definition of a session and the generation of all variables is in `/models/session.py`

### Constraints
The mandatory constraints that make a solution make sense live under `/constraints/mandatory.py`

I also started adding desiderata in `/constraints/desiderata.py`. The current approach uses an objective function that is run in pure Python and of which the solver has no knowledge about. You can see my struggles trying to write it as a linear expression that it could understand 😅.

### Views
The solutions are currently only printed to the standard output. The logic for this can be found under `/views`.

### Solver
The whole contraption is orchestrated from `/solvers/solver.py`

There are no true tests yet but you can currently see the results of the solution search by running:

```
$ ptw tests/solver
``` 

This will print the first solution found. [`ptw`](https://pypi.org/project/pytest-watch/) is a filesystem watcher, so you can play about with the data or the code and see the results after recaltulating.

In the same file where these 2 lines are:

```python
    solver.SolveWithSolutionCallback(constrained_model, solution_printer)
    # solver.SearchForAllSolutions(constrained_model, solution_printer)
```

you can commento out the first one and uncomment the second and the engine will start looking for _all_ solutions, and printing on screen only the ones that get a better score for the objective function. 
Remember to kill the process, as it may take a _long_ time to find them all!


