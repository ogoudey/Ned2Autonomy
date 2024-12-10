# Ned2Autonomy

## Overall Setup
Follow the Ned2 Beginner Guide to affirm connection.

### Setup
Follow the setups of (below) Remote Control and Autonomous Control.

### Running
Run:
```
$ python3 control.py
```
The remote control state will begin, and when it is quit (hit x on the controller), the planner will take over.

## Remote Control

### Setup
Connect the XBox controller, and follow the Ned2 Beginner Guide to connect to Ned (connecting to Ned takes a while).

Around Ned, position the elements in the setting, or update the setting to new positions.

### Running
From the root directory, run the control.py python script.

```
$ python3 control.py
```
Ned then alternates between a teleoperation mode and an "autonomous" mode. From within the teleoperation mode, press X to switch to autonomous control.


