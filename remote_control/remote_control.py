import pygame
import time

button_dict = {
    0: "A", # close claw
    1: "B",  # back home
    2: "X",  #"quit",
    3: "Y",  # open claw
    5: "right bumper"  # drop arm

}

SHIFT_VAL = 0.5 #cm
shif_value = SHIFT_VAL * 0.01
wait_sec = 1
LOWEST_Z_BIG_GRIPPER = 0.115
LOWEST_Z_SM_GRIPPER = 0.1

MOVE_THRESH = 15 
GRIPPER_ROLL_THREASH = 0.1
GRIPPER_ROLL_RATIO = 0.5
GRIPPER_AXI_THREAD = 0.1

GRIPPER_SPEED = 100   # 100 to 1000  !!!NOT FOR NED2
MAX_GRIPPER_TORQUE_PCT = 30
MAX_GRIPPER_HOLD_TORQUE_PCT = 30

Z_OFFSET_CM = 27
MAX_DOWN_VEL_PCT = 20   # speend percentage
SENSOR_MIN_Z_SPEED = 0.035 # lowesT speed downward in z, used to judge if the machine has slowed down
SENSOR_Z_THRED = 0.20  #lowest z height

def remove_multiple_axismotion_events(events: list):
    if len(events) > 1:
        print(events)
        for i, event in enumerate(events):
            if i < len(events) - 1:
                if event.type == pygame.JOYAXISMOTION and events[i+1] == pygame.JOYAXISMOTION:
                    print(f"removed event: {events.pop(i+1)}")  # remove repeated events
    print(events)
    return events

pygame.init()

def play_game(robot):
    print(f"Ready...")
    joysticks = {}
    # This dict can be left as-is, since pygame will generate a
    # pygame.JOYDEVICEADDED event for every joystick connected
    # at the start of the program.
    # ethernet connection
    
    robot.go_back_to_home(vel_pct = 100)
    robot.led_ring.snake([15, 50, 255])
    
    # don't clear all event, or the deveice can't be added
    pygame.event.clear(eventtype= pygame.JOYBUTTONDOWN)  # clear all events queued outside of this function
    pygame.event.clear(eventtype= pygame.JOYAXISMOTION)  # clear all events queued outside of this function
    pygame.event.clear(eventtype=pygame.JOYBUTTONUP)
    
    done = False
    print("Go!")
    while not done:
        # Event processing step.
        # Possible joystick events: JOYAXISMOTION, JOYBALLMOTION, JOYBUTTONDOWN,
        # JOYBUTTONUP, JOYHATMOTION, JOYDEVICEADDED, JOYDEVICEREMOVED
        
        # events = remove_multiple_axismotion_events(events=pygame.event.get())
        init_gripper_turn = 0
        for event_idx, event in enumerate(pygame.event.get()):
            if event.type == pygame.QUIT:
                done = True  # Flag that we are done so we exit this loop.
            
            if event.type == pygame.JOYBUTTONDOWN:
                print(f"Joystick button {button_dict[event.button]} pressed.")
                if event.button == 0:  # A
                    robot.close_gripper()
                    # print(f"event: {event}")
                    # print(f"joysticks:{joysticks}")
                    # print(f"joints value in radians [joint1, ..., joint6]: \n {[round(j, 4) for j in robot.arm.get_joints()]}")
                    # print(f"end effector link pose (x, y & z are expressed in meters / roll, pitch & yaw are expressed in radians): \n {np.round(robot.arm.pose.to_list(), 3)}")
                elif event.button == 3:  # Y
                    robot.open_gripper()
                    
                elif event.button == 5:  # right bumper
                    # pygame.event.clear(eventtype= pygame.JOYBUTTONDOWN) 
                    print("right bumper: drop arm!")
                    robot.drop_and_monitor()
                    time.sleep(0.5)
                    robot.raise_and_monitor()
                    robot.led_ring.snake([15, 50, 255])

                elif event.button == 1:  # B, go back
                    print(f"Going back home!")
                    robot.go_back_to_home(vel_pct = 100)
                # elif event.button == 4:  # left bumper, abort fixme: not async
                #     print(f"Stop moving!")
                #     robot.arm.stop_move()
                elif event.button == 2:  # x, quit game
                    print(f"Quit game!")
                    robot.go_back_to_home(vel_pct = 100)
                    done = True
                
            # move around
            if event.type == pygame.JOYAXISMOTION:
                # e.g., {'joy': 0, 'instance_id': 0, 'axis': 3, 'value': 0.02630695516830958})>
                joystick = pygame.joystick.Joystick(event.joy)
                
                if event.axis in [3]: # right axis, ignore vertical motion. turn claw
                    axis = joystick.get_axis(3)  # horizontal
                    if abs(axis) > GRIPPER_AXI_THREAD:
                        if init_gripper_turn == 0:
                            init_gripper_turn = axis
                        else:
                            if abs(init_gripper_turn - axis) <= 0.1:  # avoid repeating axis movement
                                continue
                        jog_pose = [0,0,0,0,0,0]
                        if axis < 0:
                            turn = max(axis * GRIPPER_ROLL_RATIO, -GRIPPER_ROLL_THREASH)
                        else:
                            turn = min(axis * GRIPPER_ROLL_RATIO, GRIPPER_ROLL_THREASH)  
                        jog_pose[5] = turn 
                        print(f"turn claw: {turn}")
                        robot.arm.jog_pose(jog_pose) 
                        
                        break # one event 

                elif event.axis in [0, 1]:  # left axis, move arm
                    axis_0 = joystick.get_axis(1)  # vertial -> x axis of robot
                    axis_1 = joystick.get_axis(0)  # horizontal -> y axis of robot
                    amply = 1
                    if abs(axis_0) > 0.5 or abs(axis_1) > 0.5:
                        jog_pose = [0,0,0,0,0,0]
                        # print(f"move x: {axis_0}")
                        # print(f"move y: {axis_1}")
                        # print(f"shift in x: {shif_value * (axis_0) * 100}cm")
                        # print(f"shift in y: {shif_value * (-axis_1) * 100}cm")
                        if axis_0 > 0:
                            jog_pose[0] = min(shif_value * axis_0 * amply, MOVE_THRESH/100)
                        else:
                            jog_pose[0] = max(shif_value * axis_0 * amply, -MOVE_THRESH/100)
                        if axis_1 > 0:
                            jog_pose[1] = min(shif_value * axis_1 * amply, MOVE_THRESH/100)
                        else:
                            jog_pose[1] = max(shif_value * axis_1 * amply, -MOVE_THRESH/100)
                        # print(f"jog pose in x, y: {jog_pose[:2]}")
                        robot.arm.jog_pose(jog_pose)
                        break
                
        
            # if event.type == pygame.JOYBUTTONUP:
            #     print(f"Joystick button {event.button} released.")

            # Handle hotplugging
            if event.type == pygame.JOYDEVICEADDED:
                # This event will be generated when the program starts for every
                # joystick, filling up the list without needing to create them manually.
                joy = pygame.joystick.Joystick(event.device_index)
                joysticks[joy.get_instance_id()] = joy
                print(f"Joystick {joy.get_instance_id()} connected")

            if event.type == pygame.JOYDEVICEREMOVED:
                del joysticks[event.instance_id]
                print(f"Joystick {event.instance_id} disconnected")
        
        # time.sleep(0.5) # avoid getting too many events, especially aximotions
    robot.led_ring.breath([15, 50, 255], 2, 100, False)
    robot.robot.end()  # close robot connection
    print(F"Robot disconnected. QUIT GAME.")
