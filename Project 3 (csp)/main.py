import MRV
from puzzle import Puzzle


def backtrack_search():
    assignment = puzzle.variables.copy()
    return solve(assignment)


def solve(assignment):

    assigned_count = len(list(filter(lambda x: type(x) is str, assignment.values())))
    if assigned_count == puzzle.N*puzzle.M:
        return assignment if puzzle.isAssignmentComplete(assignment) else False

    
    # heuristics
    # var = var_selector(assignment) # simple backtrack
    var = MRV.mrv(puzzle, assignment)  # MRV heuristic


    for value in puzzle.domain:
        if puzzle.isConsistent(var, value, assignment):
            assignment[var] = value
            result = solve(assignment)
            if result:
                return result

        assignment[var] = puzzle.variables[var]
    
    return False



def var_selector(assignment):
    for key in assignment.keys():
        if type(assignment[key]) is int:
            return key 

    return None



if __name__ == "__main__":

    puzzle = Puzzle("input/input1_method1.txt")
    puzzle.board = backtrack_search()
    puzzle.print()

            

    
