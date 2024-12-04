import pygame
from pyniryo2 import *
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
        self.A_prev = False # This should be replaced. NiryoRobot should be wrapped by AutoNiryo
        self.controller = {
            2: "X",  #"quit",
        }
        self.joysticks = {}
        pygame.init()

    
    def loop(self):

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
                    self.dx += axis_x/1000
                    self.dy += axis_y/1000
                    self.dz += axis_z/1000
                    
                    self.dx = self.dx * .99
                    self.dy = self.dy * .99
                    self.dz = self.dz * .99
                    
                    if self.dx < 1 and self.dy < 1 and self.dz < 1\
                        and self.dx > -1 and self.dy > -1 and self.dz > -1:
                        self.toy.arm.jog_pose([self.dx, self.dy, self.dz, 0, 0, 0])
                    else:
                        print("Too fast!!")
                    
                    """
                    # Safety check on code
                    if axis_x > 1 or axis_y > 1 or axis_z > 1:
                        # Input too fast!!
                        continue

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
    
if __name__ == "__main__":
    g = Game("thing controlled with xbox controller")
    g.play()

