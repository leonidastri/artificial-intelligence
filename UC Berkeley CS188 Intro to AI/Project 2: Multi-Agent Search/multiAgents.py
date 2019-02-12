# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        # keep manhattan distances from newPos to all foods left
        # with priority
        foods_distances_pq = util.PriorityQueue()
        # keep distances from newPos to every ghost with priority
        ghost_distances_pq = util.PriorityQueue()
        # value initialized with game state score
        value = successorGameState.getScore()

        for food in newFood.asList():
            dist = manhattanDistance(newPos, food)
            foods_distances_pq.push(dist,dist)

        for ghost in newGhostStates:
            ghost_pos = ghost.getPosition()
            dist = manhattanDistance(newPos, ghost_pos)
            ghost_distances_pq.push(dist,dist)

        # If foods left
        if( not foods_distances_pq.isEmpty() ):

            # find closest food
            min_food = foods_distances_pq.pop()

            # if we are in food position, that is good, maximum score
            if( min_food == 0):
                return float("inf")
            # if we are not, the closer the food is the better is the score
            # that is why we divide with min_food and we add it to value
            else:
                value += (10/min_food)

        # if there are ghosts
        if( not ghost_distances_pq.isEmpty() ):

            min_ghost = ghost_distances_pq.pop()

            # if we are in ghost position, that is bad, minimum score
            if( min_ghost == 0 ):
                return -float("inf")
            # if we are not, the closer the ghost is the worse is the score
            # that is why we divide with min_ghost and we subtract it from value
            else:
                value -=  (20/min_ghost)

        # return score
        return value

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    # followed instructor's notes, implementing of notes' functions
    pacmanIndex = 0
    starting_depth = 0

    # check if we have terminal state
    def terminal_test(self, gameState, cur_index, cur_depth):

        actions = gameState.getLegalActions(cur_index)
        terminate = (len(actions) == 0) or (cur_depth == self.depth)

        return terminate

    # find successor
    def result(self, gameState, action, cur_index):

        successor = gameState.generateSuccessor(cur_index, action)

        return successor

    # find minimax decision( implemented like instructor's function )
    def minimax_decision(self, gameState, cur_index):

        arg_max = float("-inf")
        arg_max_action = None
        cur_depth = self.starting_depth

        actions = gameState.getLegalActions(cur_index)

        for action in actions:

            successorState = self.result(gameState,action,cur_index)
            next_index = cur_index + 1
            value = self.min_value(successorState, next_index,cur_depth)

            if( arg_max < value ):
                arg_max = value
                arg_max_action = action

        return arg_max_action

    # find max value out of two values
    def find_max(self, max_v, value):

        if( value > max_v ):
            max_v = value

        return max_v

    def max_value(self, gameState, cur_index, cur_depth):

        # whenever we are in max we increase the depth
        cur_depth += 1

        # we check if terminal state
        if( self.terminal_test(gameState,cur_index,cur_depth) ):
            return self.evaluationFunction(gameState)

        max_v = float("-inf")
        actions = gameState.getLegalActions(cur_index)

        for action in actions:

            successorState = self.result(gameState,action,cur_index)
            next_index = cur_index + 1
            value = self.min_value( successorState, next_index, cur_depth)
            max_v = self.find_max(max_v,value)

        return max_v

    # find min value out of two values
    def find_min(self, min_v, value):

        if( value < min_v ):
            min_v = value

        return min_v

    def min_value(self, gameState, cur_index, cur_depth):

        # check if terminal state
        if( self.terminal_test(gameState,cur_index,cur_depth) ):
            return self.evaluationFunction(gameState)

        min_v = float("inf")
        actions = gameState.getLegalActions(cur_index)

        # get number of ghosts
        no_ghosts = gameState.getNumAgents()-1
        # number of checked ghosts
        all_ghosts_checked = (cur_index == no_ghosts)

        for action in actions:

            successorState = self.result(gameState,action,cur_index)

            # if not all ghosts checked call min again for next ghost
            if( not all_ghosts_checked ):

                next_index = cur_index + 1
                value = self.min_value(successorState,next_index,cur_depth)
                min_v = self.find_min(min_v,value)

            # else if all ghosts checked call max
            else:

                new_index = self.pacmanIndex
                # call max_value for pacman
                value = self.max_value(successorState, new_index, cur_depth)
                min_v = self.find_min(min_v,value)

        return min_v

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        # find minimax decision and return
        return self.minimax_decision(gameState, self.index)

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """
    pacmanIndex = 0
    starting_depth = 0

    # check if we have terminal state
    def terminal_test(self, gameState, cur_index, cur_depth):

        actions = gameState.getLegalActions(cur_index)
        terminate = (len(actions) == 0) or (cur_depth == self.depth)

        return terminate

    # find successor
    def result(self, gameState, action, cur_index):

        successor = gameState.generateSuccessor(cur_index, action)

        return successor

    # alphabeta decision
    def alphabeta(self, gameState, cur_index):

        arg_max = float("-inf")
        arg_max_action = None
        cur_depth = self.starting_depth
        a = float("-inf")
        b = float("inf")

        actions = gameState.getLegalActions(cur_index)

        for action in actions:

            successorState = self.result(gameState,action,cur_index)
            next_index = cur_index + 1
            value = self.min_value(successorState, next_index,cur_depth,a,b)

            if( arg_max < value ):
                arg_max = value
                arg_max_action = action

            # if value greater than b stop
            if( value > b):
                return arg_max_action

            # update a
            a = self.find_max(a,value)

        return arg_max_action

    # find max value out f 2 values
    def find_max(self, max_v, value):

        if( value > max_v ):
            max_v = value

        return max_v

    def max_value(self, gameState, cur_index, cur_depth,a,b):

        # if we in max increase deth
        cur_depth += 1

        # check if terminal state
        if( self.terminal_test(gameState,cur_index,cur_depth) ):
            return self.evaluationFunction(gameState)

        max_v = float("-inf")
        actions = gameState.getLegalActions(cur_index)

        for action in actions:

            successorState = self.result(gameState,action,cur_index)
            next_index = cur_index + 1
            # call min_value for next agent current depth
            value = self.min_value( successorState, next_index, cur_depth,a,b)
            max_v = self.find_max(max_v,value)

            # if value > b just stop and return
            if( value > b):
                return value

            # update a
            a = self.find_max(a,value)

        return max_v

    # find min of two values
    def find_min(self, min_v, value):

        if( value < min_v ):
            min_v = value

        return min_v

    def min_value(self, gameState, cur_index, cur_depth,a,b):

        # check if terminal state
        if( self.terminal_test(gameState,cur_index,cur_depth) ):
            return self.evaluationFunction(gameState)

        min_v = float("inf")
        actions = gameState.getLegalActions(cur_index)

        # get number of ghosts
        no_ghosts = gameState.getNumAgents()-1
        # check if all ghosts checked
        all_ghosts_checked = (cur_index == no_ghosts)

        for action in actions:

            successorState = self.result(gameState,action,cur_index)

            # if not checked
            if( not all_ghosts_checked ):

                next_index = cur_index + 1
                # call min_value for next agent but in current depth
                value = self.min_value(successorState,next_index,cur_depth,a,b)
                min_v = self.find_min(min_v,value)
            #lese if all ghosts checked
            else:

                new_index = self.pacmanIndex
                # call mac_value for pacman
                value = self.max_value(successorState, new_index, cur_depth,a,b)
                min_v = self.find_min(min_v,value)

            # if value < a return
            if( value < a):
                return value

            # update b
            b = self.find_min(b,value)

        return min_v

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """

        "*** YOUR CODE HERE ***"
        #return alphabeta decision
        return self.alphabeta(gameState, self.index)

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """
    pacmanIndex = 0
    starting_depth = 0

    # check if we have terminal state
    def terminal_test(self, gameState, cur_index, cur_depth):

        actions = gameState.getLegalActions(cur_index)
        terminate = (len(actions) == 0) or (cur_depth == self.depth)

        return terminate

    # find successor
    def result(self, gameState, action, cur_index):

        successor = gameState.generateSuccessor(cur_index, action)

        return successor

    # expectimax decision
    def expectimax(self, gameState, cur_index):

        arg_max = float("-inf")
        arg_max_action = None
        cur_depth = self.starting_depth

        actions = gameState.getLegalActions(cur_index)

        # for every legal action
        for action in actions:

            successorState = self.result(gameState,action,cur_index)
            next_index = cur_index + 1
            value = self.expect_value(successorState, next_index,cur_depth)

            # as instructor's notes min
            if( arg_max < value ):
                arg_max = value
                arg_max_action = action

        return arg_max_action

    # find max value out of two values
    def find_max(self, max_v, value):

        if( value > max_v ):
            max_v = value

        return max_v

    def max_value(self, gameState, cur_index, cur_depth):

        # when in max increase depth
        cur_depth += 1

        # check if terminal state
        if( self.terminal_test(gameState,cur_index,cur_depth) ):
            return self.evaluationFunction(gameState)

        max_v = float("-inf")
        actions = gameState.getLegalActions(cur_index)

        for action in actions:

            successorState = self.result(gameState,action,cur_index)
            next_index = cur_index + 1
            # call expect value for next agent but in current depth
            value = self.expect_value( successorState, next_index, cur_depth)
            max_v = self.find_max(max_v,value)

        return max_v

    # find min value out of two values
    def find_min(self, min_v, value):

        if( value < min_v ):
            min_v = value

        return min_v

    def expect_value(self, gameState, cur_index, cur_depth):

        # check if terminal state
        if( self.terminal_test(gameState,cur_index,cur_depth) ):
            return self.evaluationFunction(gameState)

        actions = gameState.getLegalActions(cur_index)
        div = len(actions)

        # get number of ghosts
        no_ghosts = gameState.getNumAgents()-1
        # check if all ghosts were checked
        all_ghosts_checked = (cur_index == no_ghosts)

        returned_value = 0.0

        for action in actions:

            successorState = self.result(gameState,action,cur_index)

            # if not all checked
            if( not all_ghosts_checked ):

                next_index = cur_index + 1
                # call expect_value for next agent but in current depth
                value = self.expect_value(successorState,next_index,cur_depth)

            else:

                new_index = self.pacmanIndex
                # call max_value for pacman
                value = self.max_value(successorState, new_index, cur_depth)

            returned_value = returned_value + value

        return returned_value * (1.0/div)

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """

        "*** YOUR CODE HERE ***"
        # return expectimax
        return self.expectimax(gameState, self.index)

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    pos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    "*** YOUR CODE HERE ***"
    # keep distances from current position to all foods
    # left with priority
    foods_distances_pq = util.PriorityQueue()
    # keep distances from current position to all ghosts
    # with priority
    ghost_distances_pq = util.PriorityQueue()
    # keep distances from current position to all scared
    # ghosts with priority
    scared_ghost_distances_pq = util.PriorityQueue()

    # initialize with current state score
    value = currentGameState.getScore()

    # keep distances to foods
    for food in newFood.asList():
        dist = manhattanDistance(pos, food)
        foods_distances_pq.push(dist,dist)

    # keep distances to ghosts
    for ghost in newGhostStates:
        ghost_pos = ghost.getPosition()
        dist = manhattanDistance(pos, ghost_pos)
        ghost_distances_pq.push(dist,dist)

    # keep distances to scared ghosts
    for ghost in newGhostStates:

        # if ghost is scared
        if( ghost.scaredTimer > 0):
            ghost_pos = ghost.getPosition()
            dist = manhattanDistance(pos, ghost_pos)
            scared_ghost_distances_pq.push(dist,dist)

    # if there are foods left
    if( not foods_distances_pq.isEmpty() ):

        min_food = foods_distances_pq.pop()

        # if we are in food, that is good, maximum score
        if( min_food == 0):
            return float("inf")
        # if we are not we need divide with min_food as the
        # closer the food is the better the score is and we add it
        else:
            value += (10/min_food)

    # if there are ghosts
    if( not ghost_distances_pq.isEmpty() ):

        min_ghost = ghost_distances_pq.pop()

        # if we are in a ghost, that is bad, minimum score
        if( min_ghost == 0 ):
            return -float("inf")
        # the closer we are the worse it is, so that is why we divide
        # with min_ghost and subtract it from score
        else:
            value -=  (20/min_ghost)

    # if there are scared ghosts
    if( not scared_ghost_distances_pq.isEmpty() ):

        min_scared_ghost = scared_ghost_distances_pq.pop()

        # if we are in scared ghost, that is good, maximum score
        if( min_scared_ghost == 0 ):
            return +float("inf")
        # else the closer the scared ghost is the better it is that is
        # why we divide with min_scared_ghost and add it to score
        else:
            value +=  (80/min_scared_ghost)

    # return score
    return value

# Abbreviation
better = betterEvaluationFunction

