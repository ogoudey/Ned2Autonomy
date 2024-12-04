from pyniryo2 import *
import os
import sys
sys.path.append(os.getcwd() + "/task1")
import core as c          # planning core

from importlib import reload



class Task:
    
    def __init__(self, robot=None):
        if not robot:
            self.robot = NiryoRobot("169.254.200.201") # Assuming ethernet!
        else:
            self.robot = robot

    
    def end(self):
        self.robot.end()
      
    def move(self, l_from, l_to):
		#print("Actually moving from %s to %s" % (l_from, l_to))
	    self.robot.arm.move_joints(l_to)
	
    def carry(self, l_from, l_to):
		#print("Actually carrying from %s to %s" % (l_from, l_to))
        self.robot.arm.move_joints(l_to)
        # carrying with torque tacit here
        
    def grasp(self, l):
		#print("Grasping " + str(l))
        self.robot.tool.close_gripper()
		
    def drop(self, l):
        self.robot.tool.open_gripper()

    def execute(self, plan, goals):
        
        print("Executing plan towards goal: " + str(goals))
        l1 = [0.0, -0.5, -0.5, 0.0, -0.5, 0.0]

        l2 = [0.0, -0.0, 0.1, 0.0, -1.5, 0.0]

        l3 = [1.0, -0.0, 0.1, 0.0, -1.5, 0.0]

        l4 = [1.0, -0.5, -0.5, 0.0, -0.5, 0.0]
        # Align initials (move block too).
        
        #self.move(None, l2) # not sure I want this...
        
        for action in plan.actions:
			#check
			#replan
            exec("self." + str(action))
		
        print("Goal reached.")	
		
		 
    def start(self):
        p = c.PlanningProblem(None)
        plan = p.solve()
        self.execute(plan, p.problem.goals)
