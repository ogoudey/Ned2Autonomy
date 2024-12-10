from task1 import task
from teleop import game
from pyniryo2 import *

if __name__ == "__main__":
    
    ned = NiryoRobot("169.254.200.201") # Assuming ethernet!
    print("A to activate gripper")
    while True:
        g = game.Game(ned)
        switch = g.loop()
        while not switch:
            
            switch = g.loop()
        print("Switching to autopilot...")
        t = task.Task(ned) # initializes NiryoRobot
        t.start() # makes plan and executes it
        print("Switching to teleoperation...")
    
