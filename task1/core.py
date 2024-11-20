import unified_planning
from unified_planning.shortcuts import *
# import niryo2

class PlanningDomain():
	def __init__(self):
		# create domain
		"""
		Location = UserType('Location')
		g_at = unified_planning.model.Fluent('g_at', BoolType(), l=Location)
		block_at = unified_planning.model.Fluent('block_at', BoolType(), l=Location)
		connected = unified_planning.model.Fluent('connected', BoolType(), l_from=Location, l_to=Location)
		closed = unified_planning.model.Fluent('closed', BoolType())
		
		move = unified_planning.model.InstantaneousAction('move', l_from=Location, l_to=Location)
		l_from = move.parameter('l_from')
		l_to = move.parameter('l_to')
		move.add_precondition(connected(l_from, l_to))
		move.add_precondition(robot_at(l_from))
		move.add_effect(g_at(l_from), False)
		move.add_effect(g_at(l_to), True)
		move.add_effect(block_at(l_from), False, grasped())
		move.add_effect(block_at(l_to), True, grasped())
		
		close = unified_planning.model.InstantaneousAction('close', l=Location)
		l = close.parameter('l_at')
		
		close.add_precondition(Not(closed()))
		close.add_effect(closed(), True)
		close.add_effect(grasped(), True, And(block_at(l), g_at(l)))
		"""

class PlanningProblem():
	def __init__(self, domain):
		# create domain
		Location = UserType('Location')
		g_at = unified_planning.model.Fluent('g_at', BoolType(), l=Location)
		block_at = unified_planning.model.Fluent('block_at', BoolType(), l=Location)
		connected = unified_planning.model.Fluent('connected', BoolType(), l_from=Location, l_to=Location)
		closed = unified_planning.model.Fluent('closed', BoolType())
		grasped = unified_planning.model.Fluent('grasped', BoolType())
		
		move = unified_planning.model.InstantaneousAction('move', l_from=Location, l_to=Location)
		l_from = move.parameter('l_from')
		l_to = move.parameter('l_to')
		move.add_precondition(connected(l_from, l_to))
		move.add_precondition(g_at(l_from))
		move.add_effect(g_at(l_from), False)
		move.add_effect(g_at(l_to), True)
		
		carry = unified_planning.model.InstantaneousAction('carry', l_from=Location, l_to=Location)
		l_from = move.parameter('l_from')
		l_to = move.parameter('l_to')
		carry.add_precondition(connected(l_from, l_to))
		carry.add_precondition(g_at(l_from))
		carry.add_precondition(block_at(l_from))
		carry.add_precondition(grasped())
		carry.add_effect(g_at(l_from), False)
		carry.add_effect(g_at(l_to), True)
		carry.add_effect(block_at(l_from), False)
		carry.add_effect(block_at(l_to), True)
		
		#move.add_effect(block_at(l_from), False, grasped())	CONDITIONAL EFFECTS
		#move.add_effect(block_at(l_to), True, grasped())
		
		close = unified_planning.model.InstantaneousAction('close', l=Location)
		l = close.parameter('l')
		
		#close.add_precondition(Not(closed()))	NEG CONDITION
		close.add_effect(closed(), True)
		
		grasp = unified_planning.model.InstantaneousAction('grasp', l=Location)
		l = grasp.parameter('l')
		grasp.add_precondition(g_at(l))
		grasp.add_precondition(block_at(l))
		grasp.add_effect(grasped(), True)
		
		
		#instantiate objects
		problem = unified_planning.model.Problem('arm')
		problem.add_fluent(g_at, default_initial_value=False)
		problem.add_fluent(connected, default_initial_value=False)
		problem.add_fluent(closed, default_initial_value=False)
		problem.add_fluent(grasped, default_initial_value=False)
		problem.add_action(move)
		problem.add_action(close)
		l1 = unified_planning.model.Object('l1', Location)
		l2 = unified_planning.model.Object('l2', Location)
		l3 = unified_planning.model.Object('l3', Location)
		l4 = unified_planning.model.Object('l4', Location)
		problem.add_object(l1)
		problem.add_object(l2)
		problem.add_object(l3)
		problem.add_object(l4)
		problem.set_initial_value(g_at(l1), True)
		problem.set_initial_value(block_at(l4), True)
		problem.set_initial_value(connected(l1, l2), True)
		problem.set_initial_value(connected(l2, l3), True)
		problem.set_initial_value(connected(l3, l4), True)
		problem.add_goal(And(g_at(l1),block_at(l1)))
		self.problem = problem
		print(problem)
	
	def solve(self):
		problem = self.problem
		with OneshotPlanner(problem_kind=problem.kind) as planner:
			result = planner.solve(problem)
			print("%s returned: %s" % (planner.name, result.plan))
	
if __name__ == "__main__":
	#domain = PlanningDomain()
	planning_problem = PlanningProblem(None)
	problem = planning_problem.problem
	with OneshotPlanner(problem_kind=problem.kind) as planner:
		result = planner.solve(problem)
		print("%s returned: %s" % (planner.name, result.plan))
		
		
	# parse plan
	# Do movement
	

