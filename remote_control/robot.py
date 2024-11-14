import pygame
#from pynput import keyboard
import numpy as np
from pyniryo2 import *
import threading
import time


GRIPPER_SPEED = 100   # 100 to 500
MAX_GRIPPER_TORQUE_PCT = 20
MAX_GRIPPER_HOLD_TORQUE_PCT = 20
Z_OFFSET_CM = 27
MAX_DOWN_VEL_PCT = 20
SENSOR_MIN_Z_SPEED = 0.05 # lowesT speed downward in z, used to judge if the machine has slowed down
SENSOR_Z_THRED = 0.25  #lowest z height

SOUND_DICT = {
        "at_top": {"sound_name": "ready.wav", "wait_end": False, "start_time_sec": 0, "end_time_sec": 2},
	    "ready_to_drop": {"sound_name": "calibration.wav", "wait_end": False, "start_time_sec": 0, "end_time_sec": 1},
	    "ready_to_grab": {"sound_name": "connected.wav", "wait_end": False, "start_time_sec": 0, "end_time_sec": 2},
	    }
    

def stop_callback(result):
    if result["status"] < RobotErrors.SUCCESS.value:
        print("stop arm Succeeded")
    else:
        print("stop arm Failed")

class NedAsyncRobot:
    
    
    SHIFT_VAL = 0.5 #cm
    shif_value = SHIFT_VAL * 0.01
    wait_sec = 1
    LOWEST_Z_BIG_GRIPPER = 0.115
    LOWEST_Z_SM_GRIPPER = 0.1

    def __init__(self, ned_ip, z_offset_cm=Z_OFFSET_CM, lowest_z = LOWEST_Z_BIG_GRIPPER, max_down_velocity_pct=MAX_DOWN_VEL_PCT,
                 gripper_speed = GRIPPER_SPEED, max_gripper_torque_pct=MAX_GRIPPER_TORQUE_PCT, max_gripper_hold_torque_pct=MAX_GRIPPER_HOLD_TORQUE_PCT,
                 sensor_min_z_speed=SENSOR_MIN_Z_SPEED, sensor_z_thresh=SENSOR_Z_THRED):

        # customized threads
        self.sense_stop_event = threading.Event() 
        self.grab_event = threading.Event()
        self.claw_event = threading.Event()
        
        self.gripper_closed = False
        
        # setup robot objects
        self.robot = NiryoRobot(ned_ip)  # connect to Ned
        print(f"Robot connected: {ned_ip}")
        ros_instance = NiryoRos(ned_ip)
        self.arm = Arm(ros_instance)  # for arm movement
        self.tool = Tool(ros_instance)  # for gripper/end effector
        self.tool.update_tool()
        self.led_ring = LedRing(ros_instance)  # for LED ring light
        self.sound = Sound(ros_instance)  # for sound 

        self.arm.calibrate_auto()  # automatically calibrate the robot, normaly only after the first connection
        client = self.robot.arm.client
        # track ROS topics via pyniryo
        self.robot_state_topic = NiryoTopic(client, '/niryo_robot/robot_state', 'niryo_robot_msgs/RobotState')
        # self.joint_states_topic = NiryoTopic(client, '/joint_states', 'sensor_msgs/JointState')
        # self.arm_max_velocity = NiryoTopic(client, 'niryo_robot/max_velocity_scaling_factor', 'std_msgs/Int32')
        
        pi=3.14
        self.orig_js = [0.0, 0.0, 0.0, 0.0, -pi/2, 0]  # home poistion
        self.down_velocity_pct = max_down_velocity_pct  # maximum velocity when the arm drops. slow for safety
        self.z_offset = -z_offset_cm * 0.01 # vertical drop distance in meter, from home position to the lowest point
        self.lowest_z = lowest_z  # set the lowest z position for safety 
        self.sensor_min_z_speed = sensor_min_z_speed   # stop the robot if it's speed is unexpectly lower(e.g., hit obstacles) than this threshold. 
        self.sensor_z_thresh = sensor_z_thresh  # start sensing for stopping after this point (e.g., sense speed change after this point)

        # gripper
        self.gripper_speed = gripper_speed #100-1000  # it doesn't work for Ned2. the speed of closing the gripper
        self.max_gripper_torque_pct = MAX_GRIPPER_TORQUE_PCT
        self.max_gripper_hold_torque_pct = max_gripper_hold_torque_pct
    def go_back_to_home(self, vel_pct = 100):
        """back to the home position and open the gripper"""
        self.arm.set_arm_max_velocity(vel_pct)
        self.arm.move_joints(self.orig_js)
        self.open_gripper()

    def raise_and_monitor(self):
        """public call to move arm up. set up the thread"""
        # print(f"raise arm", flush=True)
        releast_thread = threading.Thread(target=self._async_release_toy)
        releast_thread.start()
        self._raise_arm_and_wait()
        releast_thread.join()
    
    def drop_and_monitor(self):
        """publich call to move arm down. set up the tread """
        stop_sensor_thread = threading.Thread(target=self._async_sense_stop)
        stop_sensor_thread.start()
    
        self._move_joints_down()
        
        stop_sensor_thread.join()

    def _raise_arm_and_wait(self, vel_pct = 100):
        """raise the arm back to the home position. Then trigger _async_release_toy() that waits for the user to open the gripper """
        self.arm.set_arm_max_velocity(vel_pct)
        self.arm.move_joints(self.orig_js)
        self.set_roll_pos = self.arm.joints_state().position[4]
        # print(f"self.set_roll_pos:{self.set_roll_pos}")  # the the roll position to sense wiggling of gripper
        self.led_ring.rainbow_chase()
        self.sound.play(**SOUND_DICT['at_top'])
        self.grab_event.set()
        
    def _async_release_toy(self):
        """when the arm is waiting at the home position during _raise_arm_and_wait() call, 
        this thread checks if the user waggles the claw or use the joystick to open the gripper """
        self.grab_event.wait()
        if self.gripper_closed is False:
            raise Exception(f"gripper is not closed after grab event!")
        print(f"Shake the toy or press Y to open the gripper!")
        while self.grab_event.is_set():
            # check if manual release
            for event in pygame.event.get():
                if event.type == pygame.JOYBUTTONDOWN:
                    if event.button == 3:  # Y button
                        print(f"Joystick button {event.button} pressed.")
                        self.open_gripper()
                        self.grab_event.clear() 
                        print(f'Toy released.', flush=True)
                        break  # break out of pygame events
                    elif event.button == 2:  # X button
                        print(f"Joystick button {event.button} pressed.")
                        self.open_gripper()
                        self.grab_event.clear() 
                        print(f'Press X again to quit game.', flush=True)
                        break  # break out of pygame events
            
            # check if the user waggles the claw
            curr_roll_pos = self.arm.joints_state().position[4]
            if abs(curr_roll_pos - self.set_roll_pos) > 0.005:
                self.open_gripper()
                self.grab_event.clear() 
                print(f'Toy released.', flush=True)
            
            time.sleep(0.001)  # Add a small sleep to avoid busy-waiting
            
    
    def _move_joints_down(self):
        """opern gripper, move the arm down to the lowest point then close the gripper. 
        during dropping, _async_sense_stop senses if it should stop earlier"""
        if self.gripper_closed is True:
            self.open_gripper()

        self.sound.play(**SOUND_DICT['ready_to_drop'])
        # Get the down pose value
        start_pose = self.arm.get_pose()
        # make sure that the robot does not drop below the threshold in case the arm drops from a lower position. 
        down_pose = start_pose.copy_with_offsets(z_offset=self.z_offset)
        if down_pose.z < self.lowest_z:
            down_pose.z = self.lowest_z

        self.arm.set_arm_max_velocity(self.down_velocity_pct) # move down slowly
        pygame.event.clear() # clear any queued event that could affect the sensing thread
        self.sense_stop_event.set()  # trigger for sensing stop 
        while self.arm.get_pose().z > down_pose.z + 0.01:  # give it a 1 cemtemeter margin  #fixme: this is a bad fix for ex stopping
            self.arm.move_pose(down_pose)  # drop 

        self.close_gripper(self.gripper_speed, self.max_gripper_torque_pct, self.max_gripper_hold_torque_pct)
        if self.sense_stop_event.is_set():
            print(f"move_pose uninterrupted. clear threading event: sense_stop_event.", flush=True)
            self.sense_stop_event.clear()

    def _async_sense_stop(self):
        """sense stopping sign when the arm is dropping during _move_joints_down call. 
        either when the arm slows down unexpectly when it bumps into something, or the user interrupts"""
        self.sense_stop_event.wait()
        
        while self.sense_stop_event.is_set():
            robot_state = self.robot_state_topic()

            robot_state_z_pos = robot_state['position']['z']
            if robot_state_z_pos <= self.lowest_z:
                print(f'Stop moving: z {abs(robot_state_z_pos)} lower than minimum: {self.lowest_z}', flush=True)
                self.sense_stop_event.clear()
                self.arm.stop_move() # stop the robot, will end current movement calls like arm.move_pose() 
                break

            z_speed= robot_state['twist']['linear']['z']
            if robot_state_z_pos<=self.sensor_z_thresh and abs(z_speed) < self.sensor_min_z_speed:
                print(f'Stop moving: abs z linear speed {abs(z_speed)} lower than minimum: {self.sensor_min_z_speed}', flush=True)
                self.sense_stop_event.clear()
                self.arm.stop_move() # stop the robot, will end current movement calls like arm.move_pose()
                break

            if not self.gripper_closed:
                for event in pygame.event.get():
                    if event.type == pygame.JOYBUTTONDOWN and event.button == 0:  # A button
                        print(f"Stop moving.: Button {event.button} pressed.")
                        self.sense_stop_event.clear()
                        self.arm.stop_move()
                    break  # get out of queue
            
            time.sleep(0.001) # Check the position at intervals

    def open_gripper(self):
        self.robot.tool.open_gripper()
        self.gripper_closed = False

    def close_gripper(self, gripper_speed=500, max_gripper_torque_pct=100, max_gripper_hold_torque_pct=30):
        self.robot.tool.close_gripper(gripper_speed, max_torque_percentage=max_gripper_torque_pct, 
                                      hold_torque_percentage=max_gripper_hold_torque_pct)
        self.gripper_closed = True

