'''
A variable in a CSP is arc-consistent if every value in its domain satisfies the variable’s binary constraints.
More formally, Xi is arc-consistent with respect to another variable Xj if for every value in the current domain Di there is some value in the domain Dj that satisfies the binary constraint on the arc (Xi,Xj).
'''


'''
AC3 algorithm:

function AC3(csp) returns csp possibly with the domains reduced
    queue, a queue with all the arcs of the CSP
    while queue not empty
         (X,Y) <- getFirst(queue)
         if RemoveConsistentValues(X,Y, csp) then
              foreach Z in neighbor(X) - {Y}
                   add to queue (Z,X)
    return csp

function RemoveConsistentValues(X, Y, csp) returns true if a value was removed
    valueRemoved <- false
    foreach x in domain(X, csp)
        if there's no value of domain(Y, csp) that satisfies the restriction between X and Y then
            remove x from domain(X, csp)
            valueRemoved <- true
    return valueRemoved

'''

# AC3 algorithm to solve magnet puzzle


def ac3(puzzle):
    queue = []
    for var in puzzle.variables:
        for neighbor in get_neighbors(var, puzzle):
            queue.append((var, neighbor))

    while queue:
        (X, Y) = queue.pop(0)
        if remove_consistent_values(X, Y, puzzle):
            for Z in get_neighbors(X, puzzle):
                if Z != Y:
                    queue.append((Z, X))



def remove_consistent_values(X, Y, puzzle):
    value_removed = False
    for x in puzzle.vars_domain[X]:
        if not consistent_values(x, Y, puzzle):
            print(X, Y, puzzle.vars_domain[X], puzzle.vars_domain[Y])
            puzzle.vars_domain[X].remove(x)
            value_removed = True

    return value_removed


def consistent_values(x, Y, puzzle):
    for y in puzzle.vars_domain[Y]:
        if x != y:
            return True
    return False


def get_neighbors(var, puzzle):
    i, j = var
    valid_neighbors = []
    neighbors = [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]
    
    for neighbor in neighbors:
        if 0 <= neighbor[0] < puzzle.N and 0 <= neighbor[1] < puzzle.M:
            valid_neighbors.append(neighbor)
    
    return valid_neighbors

