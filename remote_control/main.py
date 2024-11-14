from pyniryo2 import *
import robot as ned
import remote_control

WLAN_IP = "10.10.10.10"
ETHERNET_IP = "169.254.200.201" # or -.200
ned_ip = ETHERNET_IP # switch depending on network settings


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

SHIFT_VAL = 0.5 #cm
shif_value = SHIFT_VAL * 0.01
wait_sec = 1
LOWEST_Z_BIG_GRIPPER = 0.115
LOWEST_Z_SM_GRIPPER = 0.1

def ned_init():


	robot = ned.NedAsyncRobot(ned_ip, z_offset_cm=27, max_down_velocity_pct=20, lowest_z=LOWEST_Z_BIG_GRIPPER)

	robot.sound.play("connected.wav")
	robot.led_ring.snake([15, 50, 255])
	print("Ned connected.")

	robot.open_gripper()
	robot.close_gripper()

	sound_names = robot.sound.get_sounds()

	print("Ned status:")
	print(robot.arm.hardware_status())

	print("Ned pose:")
	print(robot.arm.get_pose())
	
	return robot

def parameters(robot):
	robot.max_gripper_hold_torque_pct = 30
	robot.max_gripper_torque_pct=30
	robot.gripper_speed=30

	robot.lowest_z = LOWEST_Z_BIG_GRIPPER  # 10 cm above the base level; 12 cm above when using the begger gripper
	robot.sensor_z_thresh = 0.20 # where to start sensing speed
	robot.sensor_min_z_speed = 0.45 # # minimal speed, relative to the max_speed

	# set up robot parameters
	pi = 3.1416
	curr_velocity_pct = 20 # percentage of maximum movement speed
	gripper_speed = 100 # speed of gripper open or close, from 100-1000
	orig_js = [0.0, 0.0, 0.0, 0.0, -pi/2, 0] # starting joint values

	# set parameters for keyboard 
	current_key = ''
	direction=''

	wait_sec = 1 #seconds before dropping arm down

	# be aware of upper-threshold of the the functions
	# jog_shift can't move over ~10cm at once
	SHIFT_VAL = 0.5 #cm
	BIG_DROP_VAL = 40 # cm

	shif_value = SHIFT_VAL * 0.01 # move <shift_val> cm in x,y,z directions
	big_drop_down = BIG_DROP_VAL * 0.01 # drop down in z cm
	
	robot.open_gripper()
	robot.close_gripper()
	
	print("Ned status:")
	print(robot.arm.hardware_status())
	
def remote_control_activate(ned):
	remote_control.play_game(ned)
	
def disconnect(robot):
    robot.robot.end()
	
	
