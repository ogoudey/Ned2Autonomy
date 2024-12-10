from task1 import task
from teleop import game
from pyniryo2 import *
from brain import predictor

import threading
import time

event = threading.Event()


def thread():
    while True:
        time.sleep(.6)
        prediction = True
        if prediction:
            event.set()
        else:
            event.clear()
            pass
        

if __name__ == "__main__":
    
    ned = NiryoRobot("169.254.200.201") # Assuming ethernet!
    #model = Predictor
    print("A to activate gripper")
    while True:
    
        g = game.Game(ned)
        switch = g.loop()
        while not event.is_set():
            switch = g.loop()
        
        
        print("Switching to autopilot...")
        
        t = task.Task(ned) # initializes NiryoRobot
        t.start() # makes plan and executes it
        print("Switching to teleoperation...")
    
