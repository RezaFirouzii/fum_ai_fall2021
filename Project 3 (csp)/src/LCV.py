

def lcv(var, assignment, puzzle):

    # get the domain of the variable
    domain = puzzle.vars_domain[var]
    
    # initialize list of tuples with constraints and values that leaves the maximum flexibility
    values = []

    # loop through the domain of the variable
    for value in domain:
        # get the number of constraints that the value satisfies
        constraints = get_constraints(var, value, assignment, puzzle)
        values.append((constraints, value))
            
    # return values sorted by constraints
    values = sorted(values, key=lambda x: x[0])
    return list(map(lambda x: x[1], values))



def get_constraints(var, value, assignment, puzzle):

    # initialize the number of constraints
    constraints = 0

    # loop through the neighbors of the variable
    for neighbor in get_neighbors(var, puzzle):
        # if the value satisfies the binary constraint on the arc (var, neighbor)
        if type(assignment[neighbor]) is str and value == puzzle.REVERSE[assignment[neighbor]]:
            # increment the number of constraints
            constraints += 1

    return constraints


def get_neighbors(var, puzzle):
    i, j = var
    valid_neighbors = []
    neighbors = [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]
    
    for neighbor in neighbors:
        if 0 <= neighbor[0] < puzzle.N and 0 <= neighbor[1] < puzzle.M:
            valid_neighbors.append(neighbor)
    
    return valid_neighbors
    