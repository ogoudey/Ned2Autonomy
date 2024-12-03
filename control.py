from remote_control import main
from task1 import task

if __name__ == "__main__":
    
    ned = main.ned_init() # fancy shi* with Ned and NedAsyncRobot initializer.
    main.parameters(ned) # sets some maybe important Ned parameters
    main.remote_control_activate(ned)
    done = False
    while not done:
        done = main.step(ned)
    main.game_end(ned)
    print("Switching to autopilot...")
    t = task.Task() # initializes NiryoRobot
    t.start() # makes plan and executes it

