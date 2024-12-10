from task1 import task
from teleop import game
from pyniryo2 import *
from brain import predictor, brain_data

import os
import threading
import time


event = threading.Event()


model_path = "brain/best_model.statedict"
data_path = "brain/data"


def thread(model, sub_feature):
    index = 0
    while True:
        index += 1
        time.sleep(1)
        if index > 5:
            print(event.is_set())
            print("Setting")
            event.set()
        print("Not setting")
        """
        time.sleep(2)
        print("Prediction detected")        
        event.set()
        
        time.sleep(.1)
        index += 1
        print(index)
        prediction = model.predict(sub_feature[index])
        if prediction[0][1] > .5:
            print("Prediction detected")
            event.set()
        else:
            #print(event.is_set())
            event.clear()
            pass
        """
        

if __name__ == "__main__":
    event.clear()
    ned = NiryoRobot("169.254.200.201") # Assuming ethernet!
    print("Loading subject data...")
    model = predictor.Predictor(model_path)
    sub_feature, __ = brain_data.read_subject_csv_binary(os.path.join(data_path, "sub_1.csv"), num_chunk_this_window_size=1488)
    th = threading.Thread(target=thread, args=[model, sub_feature])
    th.start()
    #model = Predictor
    print("A to activate gripper")
    while True:
        print("Teleoperation...")        
        g = game.Game(ned)
        switch = g.loop()
        #print(event.is_set())
        while not event.is_set():

            switch = g.loop()
        
        
        print("Switching to autopilot...")
        
        t = task.Task(ned) # initializes NiryoRobot
        t.start() # makes plan and executes it
        event.clear()
    print("Plan finished execution. Ending...")
    th.join()
    
