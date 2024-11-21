# Ned2Autonomy

## Remote Control

### Quickstart:
Follow the Ned2 Beginner Guide to affirm connection, and connect the XBox controller. Then fire up python from within /remote_control. Then run
```
>>> import main
>>> ned = main.ned_init()
>>> main.parameters(ned)
>>> main.remote_control_activate(ned)
```
and you're off.

## Autonomous Control

### Mock setup
from inside the task1 directory, fire up python.
```
>>> import core
>>> p = core.PlanningProblem(None)
>>> p.solve()
```
This is the point at which Ned is a "mock". Currently to execute the mock Ned, run
```
>>> p.execute()
```
The "actually" is supposed to signify that the printed line is the abstraction of the (actual) actions by Ned. To "realize" Ned, we would replace these print lines.


### Credit:
Code is based off of Si Liu's code for a prior project.

Ned2_beginner_guide.md is entirely from her project at this point.

## Autonomous Control
Coming soon...
