# MRV heuristic to solve magnet puzzle

def mrv(puzzle, assignment):

    # 1. find the variable with minimum remaining values
    # 2. sort the remaining values in ascending order
    
    # find the variable with minimum remaining values
    min_remaining_values = 99999
    min_remaining_values_var = None
    for var in assignment.keys():
        if type(assignment[var]) is int:
            remaining_values = get_legal_values(puzzle, assignment, var)
            if remaining_values < min_remaining_values:
                min_remaining_values = remaining_values
                min_remaining_values_var = var

    return min_remaining_values_var




def get_legal_values(puzzle, assignment, var):
    legal_values = []
    for value in puzzle.domain:
        if puzzle.isConsistent(var, value, assignment):
            legal_values.append(value)

    return len(legal_values)