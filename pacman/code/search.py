# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
	"""
	Search the deepest nodes in the search tree first.

	Your search algorithm needs to return a list of actions that reaches the
	goal. Make sure to implement a graph search algorithm.

	To get started, you might want to try some of these simple commands to
	understand the search problem that is being passed in:
	print(type(problem))
	print "Start:", problem.getStartState()
	print "Is the start a goal?", problem.isGoalState(problem.getStartState())
	"""
	startState = problem.getStartState() # get the start state
	myStack = util.Stack()# intialise a LIFO (Last In First Out Stack)
	myStack.push(( startState , [] ))  # push the starting element to the stack
	visited = []
	# if the starting element is itself the goal state then no actions required
	if problem.isGoalState(problem.getStartState()):
		return []

	while not myStack.isEmpty():
		newTuple = myStack.pop()  # get the front element of the stack
		newState = newTuple[0]
		oldActions = newTuple[1]
		# if it is already visited ignore it and move to next
		if newState in visited:
			continue
		# else add it to the visited list
		visited.append(newState)
		if problem.isGoalState(newState):
			return oldActions
		else:
			# add the successors to the Queue if they have not already been visited
			for succ in problem.getSuccessors(newState):
				if succ[0] not in visited:
					myStack.push( (succ[0] , oldActions + [succ[1]]) )
	
	print('Goal Not Found')
	return []
	"*** YOUR CODE HERE ***"
	util.raiseNotDefined()

def breadthFirstSearch(problem):
	"""Search the shallowest nodes in the search tree first."""
	"*** YOUR CODE HERE ***"
	startState = problem.getStartState() # get the start state
	myQueue = util.Queue() # intialise a FIFO (First In First Out Queue)
	myQueue.push(( startState , [] )) # push the starting element to the queue
	visited = []
	# if the starting element is itself the goal state then no actions required
	if problem.isGoalState(problem.getStartState()):
		return []

	while not myQueue.isEmpty():
		newTuple = myQueue.pop() # get the front element of the queue
		newState = newTuple[0]
		oldActions = newTuple[1]
		# if it is already visited ignore it and move to next
		if newState in visited:
			continue
		# else add it to the visited list
		visited.append(newState)
		# if this state is the goal, return the actions till now
		if problem.isGoalState(newState):
			return oldActions
		else:
			# add the successors to the Queue if they have not already been visited
			for succ in problem.getSuccessors(newState):
				if succ[0] not in visited:
					myQueue.push( (succ[0] , oldActions + [succ[1]]) )
	
	print('Goal Not Found')
	return []

def uniformCostSearch(problem):
	"""Search the node of least total cost first."""
	"*** YOUR CODE HERE ***"
	startState = problem.getStartState() # get the start state
	myPQueue = util.PriorityQueue()  # intialise a Queue ( min element pops first )
	myPQueue.update(( startState , [] ) , 0) # push the starting element to the queue
	visited = []
	# if the starting element is itself the goal state then no actions required
	if problem.isGoalState(problem.getStartState()):
		return []

	while not myPQueue.isEmpty():
		newTuple = myPQueue.pop() # get the front element of the queue
		newState = newTuple[0]
		oldActions = newTuple[1]
		# if it is already visited ignore it and move to next
		if newState in visited:
			continue
		# else add it to the visited list
		visited.append(newState)
		# if this state is the goal, return the actions till now
		if problem.isGoalState(newState):
			return oldActions
		else:
			# add the successors to the Queue if they have not already been visited
			for succ in problem.getSuccessors(newState):
				if succ[0] not in visited:
					myPQueue.update( (succ[0] , oldActions + [succ[1]]) , problem.getCostOfActions(oldActions+[succ[1]])  )
	
	print('Goal Not Found')
	return []

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
	"""Search the node that has the lowest combined cost and heuristic first."""
	"*** YOUR CODE HERE ***"
	
	startState = problem.getStartState() # get the start state
	myPQueue = util.PriorityQueue()  # intialise a Queue ( min element pops first )
	myPQueue.update(( startState , [] ) , 0 + heuristic(startState,problem) ) # push the starting element to the queue
	visited = []
	if problem.isGoalState(problem.getStartState()):
		return []

	while not myPQueue.isEmpty():
		newTuple = myPQueue.pop()
		newState = newTuple[0]
		oldActions = newTuple[1]
		# if it is already visited ignore it and move to next
		if newState in visited:
			continue
		# else add it to the visited list
		visited.append(newState)
		# if this state is the goal, return the actions till now
		if problem.isGoalState(newState):
			return oldActions
		else:
			# add the successors to the Queue if they have not already been visited
			for succ in problem.getSuccessors(newState):
				if succ[0] not in visited:
					succCost = heuristic(succ[0],problem) + problem.getCostOfActions(oldActions+[succ[1]]) 
					myPQueue.update( (succ[0] , oldActions + [succ[1]]) ,  succCost )
	
	print('Goal Not Found')
	return []

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
