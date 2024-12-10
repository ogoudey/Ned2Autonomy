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
        # switch to move-pose
	    self.robot.arm.move_joints(l_to)
	
    def carry(self, l_from, l_to):

        self.robot.arm.move_joints(l_to)

        
    def grasp(self, l):

        self.robot.tool.close_gripper()
		
    def drop(self, l):
        self.robot.tool.open_gripper()

    def execute(self, plan, goals):
        print("Executing plan towards goal: " + str(goals) + "...")
        
        """
        Preplan observation:
        A@x,y,z, B@x,y,z
        l1 = B, l2 = B_z+5, etc
            goto A, grab, goto B, drop
        
        
        
        l1, l2, l3, l4
            goto l1, grab, goto l2, goto l3, goto l4, drop
        Postplan observation:
        l1 (B) = x,y,z, l4 (A) = x,y,z
        
                
        
        
        """
        l1 = [-1.6617832, -0.4292528, -0.6855434, 0.11360723, -0.40506358, 1.40989]
        l2 = [-1.7302699, -0.07475549, -0.521929, 0.05224800, -0.93275297, 1.55863]
        l3 = [1.63775476, 0.034326995, -0.537087, -0.01371335, -0.9327529, 1.56015]
        l4 = [1.61492585, -0.5050001, -0.5537431, 0.062985, -0.5369, 1.54787926856]


        # Align initials (move block too).        
        #self.move(None, l2) # not sure I want this...
        
        for action in plan.actions:
            print("executing " + str(action))
			#check
			#replan
            exec("self." + str(action))
		
        print("Goal reached.")	
		
		 
    def start(self):
        p = c.PlanningProblem(None)
        plan = p.solve()
        print(plan)
        self.execute(plan, p.problem.goals)
