# forward checking algorithm for magnet puzzle problem

import AC3
import MRV
from puzzle import Puzzle


def backtrack_search():
    assignment = puzzle.variables.copy()
    return forward_check(assignment)


def forward_check(assignment):

    assigned_count = len(list(filter(lambda x: type(x) is str, assignment.values())))
    if assigned_count == puzzle.N*puzzle.M:
        return assignment if puzzle.isAssignmentComplete(assignment) else False

    
    # var = var_selector(assignment)     # simple backtrack
    var = MRV.mrv(puzzle, assignment)    # MRV heuristic
    var2 = puzzle.get_neighbor(var, puzzle.variables[var])
    var_domain = puzzle.vars_domain[var].copy() # returns specific var domain

    # AC3.ac3(puzzle)
    for value in var_domain:
        if puzzle.isConsistent(var, value, assignment) and puzzle.isConsistent(var2, puzzle.REVERSE[value], assignment):
            assignment[var] = value
            assignment[var2] = puzzle.REVERSE[value]

            if value != 'x' and not valid_neighbors_domain(var, assignment) and not valid_neighbors_domain(var2, assignment):
                return False
            result = forward_check(assignment)            
            if result:
                return result

        assignment[var] = puzzle.variables[var]
    
    puzzle.vars_domain[var] = puzzle.domain.copy()
    return False



def valid_neighbors_domain(var, assignment):

    value = assignment[var]
    for neighbor in get_unassigned_neighbors(var, assignment):
        try:
            puzzle.vars_domain[neighbor].remove(value)
        except:
            pass

        if not puzzle.vars_domain[neighbor]:
            return False

    return True



def get_unassigned_neighbors(var, assignment):
    i, j = var
    valid_neighbors = []
    neighbors = [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]
    
    for neighbor in neighbors:
        if 0 <= neighbor[0] < puzzle.N and 0 <= neighbor[1] < puzzle.M and type(assignment[neighbor]) is int:
            valid_neighbors.append(neighbor)
    
    return valid_neighbors



def reset_variables_domain(puzzle):
    puzzle.vars_domain = {}
    for var in puzzle.variables:
        puzzle.vars_domain[var] = puzzle.domain.copy()


def var_selector(assignment):
    for key in assignment.keys():
        if type(assignment[key]) is int:
            return key 

    return None



if __name__ == "__main__":

    puzzle = Puzzle("input/input1_method2.txt")
    reset_variables_domain(puzzle)
    puzzle.board = backtrack_search()
    puzzle.print()

            