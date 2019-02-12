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

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    # Graph search algorithm from pdf 3
    # (http://cgi.di.uoa.gr/~ys02/index.php/lectures/201-s2018-2019)

    #keep moves to return them
    solution = []
    node = problem.getStartState()

    # using stack as the instructor noted
    frontier = util.Stack()
    frontier.push((node,solution))
    explored = set([])

    while True:

        if frontier.isEmpty():
            break;

        node, solution = frontier.pop()

        # Instructor noted to check goal state right after frontier pop(3rd edition of AIMA)
        if problem.isGoalState(node):
            return solution

        explored.add(node)

        # for every successor of node
        for successor in problem.getSuccessors(node):

            # check if successor node in explored
            found_in_explored = True if successor[0] in explored else False

            # check if successor node in frontier
            found_in_frontier = False
            for entry in frontier.list:
                if entry[0] == successor[0]:
                    found_in_frontier = True
                    break
            '''
                in the pdf 3 graph search algorithm tells us that we have to check child 
                not be in explored or frontier but that does not work with autograder.py in DFS,
                so you cannot get 3/3.
            '''

            #if (not found_in_explored) and (not found_in_frontier):
            if not found_in_explored:

                #if problem.isGoalState(node):
                #    return solution + [successor[1]]
                frontier.push((successor[0], solution + [successor[1]]))

    return []

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    # Graph search algorithm from pdf 3
    # (http://cgi.di.uoa.gr/~ys02/index.php/lectures/201-s2018-2019)

    #keep moves to return them
    solution = []
    node = problem.getStartState()

    # using queue as the instructor noted
    frontier = util.Queue()
    frontier.push((node,solution))
    explored = set([])

    while True:

        if frontier.isEmpty():
            break;

        node, solution = frontier.pop()

        # Instructor noted to check goal state right after frontier pop(3rd edition of AIMA)
        if problem.isGoalState(node):
            return solution

        explored.add(node)

        # for every successor of node
        for successor in problem.getSuccessors(node):

            # check if successor is in explored
            found_in_explored = True if successor[0] in explored else False

            # check if successor is in frontier
            found_in_frontier = False
            for entry in frontier.list:
                if entry[0] == successor[0]:
                    found_in_frontier = True
                    break

            '''
                in the pdf 3 graph search algorithm tells us that we have to check child 
                not be in explored or frontier. That does work with autograder.py in BFS,
                so you can get 3/3
            '''

            if (not found_in_explored) and (not found_in_frontier):
            #if not found_in_explored:

                #if problem.isGoalState(node):
                #    return solution + [successor[1]]
                frontier.push((successor[0], solution + [successor[1]]))

    return []

def uniformCostSearch(problem):
    """Search the node of least total cost first."""

    "*** YOUR CODE HERE ***"

    # Graph search algorithm from pdf 3
    # (http://cgi.di.uoa.gr/~ys02/index.php/lectures/201-s2018-2019)
    #keep moves to return them
    solution = []
    node = problem.getStartState()
    node_path_cost = 0

    # Priority Queue where priority is the solution cost
    frontier = util.PriorityQueue()
    frontier.push((node,solution, node_path_cost), node_path_cost)
    explored = set([])

    while True:

        if frontier.isEmpty():
            break;

        node, solution, node_path_cost = frontier.pop()

        if problem.isGoalState(node):
            return solution

        # autoupgrader.py gives 0/3 because it fails in many_paths testing
        # if we want to take 3/3 we have to use this code. the instructor's
        # algorithm is in comments after this code

        if node not in explored:

            explored.add(node)

            # for every successor of node
            for successor in problem.getSuccessors(node):

                # check if successor in explored
                found_in_explored = True if successor[0] in explored else False

                # check if successor in frontier
                found_in_frontier = False
                for entry in frontier.heap:
                    if entry is successor:
                        found_in_frontier = True
                        break

                path_cost = problem.getCostOfActions(solution + [successor[1]])

                if (not found_in_explored) and (not found_in_frontier):

                    # update is used like add
                    frontier.update((successor[0], solution+[successor[1]], path_cost), path_cost)

                # if cost is better just do an update
                elif (found_in_frontier) and (path_cost < node_path_cost):

                    frontier.update((successor[0], solution+[successor[1]], path_cost), path_cost)
        '''
        explored.add(node)

        for successor in problem.getSuccessors(node):

            found_in_explored = True if successor[0] in explored else False

            found_in_frontier = False

            for entry in frontier.heap:
                if entry is successor:
                    found_in_frontier = True
                    break

            path_cost = problem.getCostOfActions(solution + [successor[1]])

            if (not found_in_explored) and (not found_in_frontier):

                frontier.update((successor[0], solution+[successor[1]], path_cost), path_cost)

            elif (found_in_frontier) and (path_cost < node_path_cost):

                frontier.update((successor[0], solution+[successor[1]], path_cost), path_cost)

            '''
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

    # Graph search algorithm from pdf 3
    # (http://cgi.di.uoa.gr/~ys02/index.php/lectures/201-s2018-2019)
    #keep moves to return them
    solution = []
    node = problem.getStartState()

    frontier = util.PriorityQueue()

    # f(n) = g(n) + h(n)
    # where g(n) cost from start to n
    # and h(n) minimum cost from n to goal state
    f_n = problem.getCostOfActions(solution) + heuristic(node,problem)
    # using fn as priority in priority queue
    frontier.push( (node,solution), f_n)

    explored = set([])

    while True:

        if frontier.isEmpty():
            break;

        node, solution = frontier.pop()

        # Instructor noted to check goal state right after frontier pop(3rd edition of AIMA)
        if problem.isGoalState(node):
            return solution

        if( node  not in explored):
            explored.add(node)

            # for every successor of node
            for successor in problem.getSuccessors(node):

                # check if successor in explored
                found_in_explored = True if successor[0] in explored else False

                # check if successor in frontier
                found_in_frontier = False
                for entry in frontier.heap:
                    if entry[0] == successor[0]:
                        found_in_frontier = True
                        break

                if (not found_in_explored) and (not found_in_frontier):

                    f_n = problem.getCostOfActions(solution+[successor[1]]) + heuristic(successor[0],problem)
                    frontier.push((successor[0], solution+[successor[1]]), f_n)
        '''
        explored.add(node)

        for successor in problem.getSuccessors(node):

            found_in_explored = True if successor[0] in explored else False

            found_in_frontier = False

            for entry in frontier.heap:
                if entry[0] == successor[0]:
                    found_in_frontier = True
                    break

            if (not found_in_explored) and (not found_in_frontier):

                f_n = problem.getCostOfActions(solution+[successor[1]]) + heuristic(successor[0],problem)
                frontier.push((successor[0], solution+[successor[1]]), f_n)
        '''

    return []

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch