from task1 import task
from teleop import game
from pyniryo2 import *
import Predictor

import threading
import time

import brain_data

event = threading.Event()

model_path = "beststatedict"
data_path = "data"


def thread():
    model = predictor.Predictor(model_path)
    sub_feature, __ = brain_data.read_subject_csv_binary(os.path.join(data_path, "sub_1.csv"), num_chunk_this_window_size=1488)
    index = 0
    while True:
        time.sleep(.6)
        index += 1
        prediction = model.predict(sub_feature(index))
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
    
