from typing import List, Tuple

from csp import *
import time
import sys

# input-file paths
inputs = ["./puzzles/puzzle1",
          "./puzzles/puzzle2",
          "./puzzles/puzzle3",
          "./puzzles/puzzle4",
          "./puzzles/puzzle5",
          "./puzzles/puzzle6",
          "./puzzles/puzzle7",
          "./puzzles/puzzle8"]

class KenKen(CSP):

    def __init__(self, input):

        self.set_total_constraints()                # initialize total constraints
        self.variables = list()                     # variables-cells of puzzle
        # Dicts with key every cell of puzzle
        self.domains = dict()                       # domains of variables-cells
        self.neighbors = dict()                     # neighbors of cells( same row, column )
        self.clique_neighbors = dict()              # neighbors of cells( same clique )
        self.clique_operation = dict()              # operation of clique( '-/add/sub/mul/div')
        self.clique_total_value = dict()            # total value of clique

        # read input for information of puzzle
        self.read_input_file(input)

        # all variables have the same domain
        # created one time for all variables
        domain = []
        for i in range(1,self.puzzle_size+1):
            domain.append(i)

        # find neighbors of same row and columns for every variable
        for i in range(0,self.puzzle_size):
            for j in range(0,self.puzzle_size):
                self.variables.append((i,j))
                self.domains[(i,j)] = domain
                var_neighbors = []
                for k in range(0,self.puzzle_size):
                    for m in range(0,self.puzzle_size):
                        if( (i,j) != (k,m) ):
                            if( (i == k) or (j == m) ):
                                var_neighbors.append((k,m))

                self.neighbors[(i,j)] = var_neighbors

        CSP.__init__(self, self.variables, self.domains, self.neighbors, self.kenken_constraint)

        # print("variables: ", self.variables)
        # print("domains: ", self.domains)
        # print("neighbors: ", self.neighbors)
        # print("clique neighbors: ", self.clique_neighbors)
        # print("clique operation: ", self.clique_operation)
        # print("clique total value: ", self.clique_total_value)

    def read_input_file(self, input):
        line_counter = 1
        file = open(input,"r")

        for line in file:

            line_info = list()
            if(line_counter == 1):
                self.puzzle_size = int(line)
            else:
                line_info_counter = 1
                team_vars = list()
                for info in line.strip().split(' '):

                    if(line_info_counter == 1):
                        op = info
                    elif(line_info_counter == 2):
                        total_value = int(info)
                    else:
                        i = int(info[1])
                        j = int(info[3])
                        team_vars.append((i,j))

                    line_info_counter += 1

                for var in team_vars:
                    self.clique_neighbors[var] = team_vars
                    self.clique_operation[var] = op
                    self.clique_total_value[var] = total_value

            line_counter += 1

    def kenken_constraint(self, A, a, B, b):

        # check if same
        if( A == B ):
            return True
        else:
            # check if in same row or column
            # and if they are and have same value  return False
            if( B in self.neighbors[A] ):
                if( a == b ):
                    return False

            clique_members = self.clique_neighbors[A]
            clique_op = self.clique_operation[A]
            # chech if A and B are in same clique
            same_clique = True if( B in clique_members ) else False

            if( clique_op == '-'):
                #print(clique_op)
                return_value = self.no_operation(A, a, same_clique)
            elif( clique_op == 'add'):
                #print(clique_op)
                return_value = self.addition(A, a, same_clique)
            elif( clique_op == 'sub'):
                #print(clique_op)
                return_value = self.subtraction(A, a, b, same_clique)
            elif( clique_op == 'mul'):
                #print(clique_op)
                return_value = self.multiplation(A, a, same_clique)
            elif( clique_op == 'div'):
                #print(clique_op)
                return_value = self.division(A, a, b, same_clique)

        self.increase_total_constraints()

        return return_value

    def no_operation(self, A, a, same_clique):

        total_value = self.clique_total_value[A]

        # if they are not the same and are on same clique
        # wrong puzzle
        if( same_clique ):
            sys.exit()
        # else A is not in clique with B
        else:
            # check if value of A equals the value of clique
            return_value = True if( a == total_value ) else False

        return return_value

    def addition(self, A, a, same_clique):

        flag = True
        return_value = True
        clique_members = self.clique_neighbors[A]
        total_value = self.clique_total_value[A]
        sum_value = a

        for member in clique_members:
            if( member != A ):
                if( member in self.infer_assignment() ):
                    sum_value += self.infer_assignment()[member]
                else:
                    flag = False

            # assigned all and value equals total value of clique
            if( flag and sum_value == total_value):
                return_value = True
            # not all assigned and value less than total value continue
            elif( not flag and sum_value < total_value ):
                return_value = True
            else:
                return_value = False

        return return_value

    # only for 2-variable cliques
    def subtraction(self, A, a, b, same_clique):

        flag = False
        return_value = True
        clique_members = self.clique_neighbors[A]
        total_value = self.clique_total_value[A]

        # if in same clique, check for b value
        if( same_clique ):
            sub_val = b
            flag = True
        # else if not in same clique, check for the other
        # variable if assigned
        else:
            for member in clique_members:
                if( member != A and member in self.infer_assignment()):
                    sub_val = self.infer_assignment()[member]
                    flag = True

        if( flag ):
            if( abs(a - sub_val) == total_value ):
                return_value = True
            else:
                return_value = False

        return return_value

    def multiplation(self, A, a, same_clique):

        flag = True
        return_value = True
        clique_members = self.clique_neighbors[A]
        total_value = self.clique_total_value[A]
        sum_value = a

        for member in clique_members:
            if( member != A ):
                if( member in self.infer_assignment() ):
                    sum_value *= self.infer_assignment()[member]
                else:
                    flag = False

        # assigned all and value equals total value of clique
        if( flag and sum_value == total_value):
            return_value = True
        # not all assigned and value less than total value continue
        elif( not flag and sum_value < total_value ):
            return_value = True
        else:
            return_value = False

        return return_value

    # only for 2-variable cliques
    def division(self, A, a, b, same_clique):

        flag = False
        return_value = True
        clique_members = self.clique_neighbors[A]
        total_value = self.clique_total_value[A]

        # if same clique, check for b value
        if( same_clique ):
            divisor = b
            flag = True
        # if not same clique, check for other variable
        # of clique if assigned
        else:
            for member in clique_members:
                if( member != A and member in self.infer_assignment()):
                    divisor = self.infer_assignment()[member]
                    flag = True

        if( flag ):
            if( a > divisor ):
                if( (float(a)/float(divisor)) == total_value):
                    return_value = True
                else:
                    return_value = False
            else:
                if( (float(divisor)/float(a)) == total_value):
                    return_value = True
                else:
                    return_value = False

        return return_value

    # print solution of puzzle
    def display(self, assignment):

        for var in self.variables:
            print(assignment[var], end = " ")
            if(var[1] == (self.puzzle_size-1) ):
                print("")

    # get total assignments
    def get_total_assignments(self):
        return self.nassigns

    def set_total_constraints(self):
        self.total_constraints = 0

    def get_total_constraints(self):
        return self.total_constraints

    def increase_total_constraints(self):
        self.total_constraints += 1

# solve kenken with every algorithm
def solve_kenken(input):

    kk = KenKen(input)
    prev_assignments = 0

    # solve puzzle with every algorithm and print
    # the info needed
    for index in range(1,7):

        print("----------")
        start = time.clock()
        if( index == 1):
            print("- BT algorithm:")
            result = backtracking_search(kk)
        elif( index == 2):
            print("- BT+MRV algorithm")
            result = backtracking_search(kk, select_unassigned_variable=mrv)
        elif( index == 3):
            print("- FC algorithm:")
            result = backtracking_search(kk, inference=forward_checking)
        elif( index == 4):
            print("- FC+MRV algorithm:")
            result = backtracking_search(kk, inference=forward_checking, select_unassigned_variable=mrv)
        elif( index == 5):
            print("- MAC algorithm:")
            result = backtracking_search(kk, inference=mac)
        elif( index == 6):
            print("- MINCONFLICTS algorithm:")
            result = min_conflicts(kk)

        if( result != None):
            kk.display(result)
        print("Time: " + str(time.clock()-start) + " seconds.")
        print("Assignemnts: " + str(kk.get_total_assignments() - prev_assignments))
        print("Constraints: " + str(kk.get_total_constraints()))
        kk.set_total_constraints()
        prev_assignments = kk.get_total_assignments()

    return

# main
if __name__ == '__main__':

    # choose puzzle to solve
    answer = input("Give a number from 1 to 8 to choose puzzle.\nGive 0 to finish.\n")
    answer = int(answer)

    while(answer != 0):

        if( answer >= 1 and answer <= 8):
            print("######################")
            print("Solution for \'puzzle"+ str(answer) + "\'")
            print("######################")
            solve_kenken(inputs[answer-1])
        answer = input("Give a number from 1 to 8 to choose puzzle.\nGive 0 to finish.\n")
        answer = int(answer)
