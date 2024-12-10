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
        l1 = [-1.661783206664591, -0.42925281244151947, -0.6855434184041744, 0.11360723189333033, -0.40506358159160216, 1.409820997656697]


        l2 = [-1.7302699265128485, -0.07475549741044729, -0.521929273005218, 0.05224800037790445, -0.9327529726242623, 1.558617134081604]


        l3 = [1.6377547629136813, 0.034320599522190354, -0.5370787309125288, -0.013713173501177955, -0.9327529726242623, 1.5601511148694898]

        l4 = [1.6149258562975954, -0.5050001019780733, -0.5537431346105706, 0.06298586589310418, -0.5369859293497674, 1.5478792685664051]
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
