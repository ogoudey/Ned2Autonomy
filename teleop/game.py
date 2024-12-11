import pygame
from pyniryo2 import *
import sys
#import threading

class Game:
    def __init__(self, toy):
        pygame.init()
        self.exit = False
        try:
            assert type(toy) == NiryoRobot
        except AssertionError:
            print("Not controlling a NiryoRobot...")
        except NameError as n:
            print(n, end="... ")
            print("of course NiryoRobot isn't defined")
        self.toy = toy
        self.toy_joints = toy.arm.get_joints()
        self.A_prev = False # This should be replaced. NiryoRobot should be wrapped by AutoNiryo
        self.controller = {
            2: "X",  #"quit",
        }
        
        self.joysticks = {}
        pygame.init()

    
    def loop(self):
        pygame.event.clear(eventtype= pygame.JOYBUTTONDOWN)
        pygame.event.clear(eventtype= pygame.JOYAXISMOTION)  # clear all events queued outside of this function
        for event in pygame.event.get():
                if event.type == pygame.JOYBUTTONDOWN:
                    #print(f"Joystick button {self.controller[event.button]} pressed.")
                    if event.button == 2:
                        print(f"Quit game!")
                        self.exit = True
                    elif event.button == 0:
                        self.toy.tool.open_gripper()    #self.toy.isopen()... self.toy.cerebellum.grip()
                        if self.A_prev:
                            self.toy.tool.open_gripper()
                            self.A_prev = False
                        else:
                            self.toy.tool.close_gripper()
                            self.A_prev = True
                            
                if event.type == pygame.JOYAXISMOTION:
                    joystick = pygame.joystick.Joystick(event.joy)
                    axis_x = joystick.get_axis(1)  # left joystick up/down = robot x
                    axis_y = joystick.get_axis(0)  # left joystick right/left = robot y
                    axis_z = joystick.get_axis(3)  # right joystick left/right = robot z
                    """
                    dx, dy, dz = norm(axis_x), norm(axis_y), norm(axis_z)
                    dj = [dx, dy, dz, 0, 0, 0]
                    print(dz)
                    
                    #self.toy.arm.jog_pose(jp)
                    self.toy_joints = [sum(x) for x in zip(self.toy_joints, dj)]

                    print("Joints " + str(self.toy_joints))
                    self.toy.arm.move_joints(self.toy_joints)
                    """
                    
                    
                    # Jerky movement.
                    if axis_x > 0.5 or axis_x < -0.5:
                        self.toy.arm.shift_pose(RobotAxis.X, axis_x / -100)
                    if axis_y > 0.5 or axis_y < -0.5:
                        self.toy.arm.shift_pose(RobotAxis.Y, axis_y / -100)
                    if axis_z > 0.5 or axis_z < -0.5:
                        self.toy.arm.shift_pose(RobotAxis.Z, axis_z / 100)
                    
                    
                if event.type == pygame.JOYDEVICEADDED:
                    joy = pygame.joystick.Joystick(event.device_index)
                    self.joysticks[joy.get_instance_id()] = joy
                    print(f"Joystick {joy.get_instance_id()} connected")
                if event.type == pygame.JOYDEVICEREMOVED:
                    del self.joysticks[event.instance_id]
                    print(f"Joystick {event.instance_id} disconnected")
        return self.exit
    
    # main loop internal to this class, for testing              
    def play(self):

        while not self.exit:    
            self.loop()
        pygame.quit()
# the lamest helper function:
# x input variable; l lower bound; k scaling factor
def norm(x, l=0.1, k=100):
    if x < l and x > -l:
        return 0
    else:
        return x / k
        
   # for testing... 
if __name__ == "__main__":
    g = Game(sys.argv[1])
    g.play()

