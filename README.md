# Ned2Autonomy

## Setup
Follow the Ned2 Beginner Guide to affirm connection.

## Control Switch
(Not confirmed... but should be able to)

Run:
```
$ python3 control.py
```
The remote control state will begin, and when it is quit (hit x on the controller), the planner will take over.

## Remote Control
Connect the XBox controller. Then fire up python from within /remote_control. Then run:
```
>>> import main
>>> ned = main.ned_init()
>>> main.parameters(ned)
>>> main.remote_control_activate(ned)
```
and you're off.

TODO: Simplify code and customize the pygame.

### Credit:
Code is based off of Si Liu's code for a prior project.

Ned2_beginner_guide.md is entirely from her project at this point.

## Autonomous Control
"Autonomous" performance is doing a somewhat prescribed task. To see the task, complete the physical setup first.

### Setup
In the MULip lab, 1. make sure the Ned base is right in the outlines (there by default), and 2. make sure the cube (or whatever) is about 1cm above the smaller outline. The planning domain assumes these relative placements.

### Running
Then from within the task1 directory fire up python and run:
```
>>> import task
>>> t = task.Task()
>>> t.start()
```
Ned should generate a plan to achieve the goal of having the cube put at a specific location in front of it. Then it executes it.


