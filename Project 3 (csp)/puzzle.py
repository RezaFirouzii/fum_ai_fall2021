from os import putenv


class Puzzle:

    def __init__(self, addr):

        self.board = {}
        self.variables = {}
        self.domain = ['+', '-', 'x']
        self.REVERSE = {
            '+': '-',
            '-': '+',
            'x': 'x'
        }

        # Read puzzle
        with open(addr, "r") as f:
            f = list(f)
            self.N, self.M = map(int, f[0].split())
            self.row_pos = list(map(int, f[1].split()))
            self.row_neg = list(map(int, f[2].split()))
            self.col_pos = list(map(int, f[3].split()))
            self.col_neg = list(map(int, f[4].split()))

            for i in range(self.N):
                row = list(map(int, f[i+5].split()))
                for j in range(self.M):
                    self.variables[i, j] = row[j]


    # constraints:
    # 1. each row has exactly "row_pos" +
    # 2. each row has exactly "row_neg" -
    # 3. each col has exactly "col_pos" +
    # 4. each col has exactly "col_neg" -
    # 5. no adjacent cells have the same value

    def isAssignmentComplete(self, assignment):
        
        rows_pos_count = [0 for _ in range(self.N)]
        rows_neg_count = [0 for _ in range(self.N)]

        for row in range(self.N):
            for col in range(self.M):
                ch = assignment[row, col]
                if ch == "+":
                    rows_pos_count[row] += 1
                elif ch == "-":
                    rows_neg_count[row] += 1
        
        
        cols_pos_count = [0 for _ in range(self.M)]
        cols_neg_count = [0 for _ in range(self.M)]

        for col in range(self.M):
            for row in range(self.N):
                ch = assignment[row, col]
                if ch == "+":
                    cols_pos_count[col] += 1
                elif ch == "-":
                    cols_neg_count[col] += 1
                    
        
        for row in range(self.N):
            if self.row_pos[row] != -1:
                if rows_pos_count[row] != self.row_pos[row]:
                    return False
            if self.row_neg[row] != -1:
                if rows_neg_count[row] != self.row_neg[row]:
                    return False
                
        
        for col in range(self.M):
            if self.col_pos[col] != -1:
                if cols_pos_count[col] != self.col_pos[col]:
                    return False
            if self.col_neg[col] != -1:
                if cols_neg_count[col] != self.col_neg[col]:
                    return False

        # for row in range(self.N):
        #     for col in range(self.M):

        #         if self.variables[row, col] == 0:
        #             if not self.is_horizontally_valid(row, col, assignment):
        #                 return False
        #         else:
        #             if not self.is_vertically_valid(row, col, assignment):
        #                 return False

        return True


    def is_horizontally_valid(self, row, col, assignment):
        
        value = assignment[row, col]
        h_neighbors = [(row, col-1), (row, col+1)]
        
        for i, j in h_neighbors:
            if 0 <= i < self.N and 0 <= j < self.M and self.variables[i, j] == 0:

                if value != assignment[i, j] and value != 'x' and assignment[i, j] != 'x':
                    return True
                if value == assignment[i, j] == 'x':
                    return True

        return False


    def is_vertically_valid(self, row, col, assignment):
        value = assignment[row, col]
        v_neighbors = [(row-1, col), (row+1, col)]
        
        for i, j in v_neighbors:
            if 0 <= i < self.N and 0 <= j < self.M and self.variables[i, j] == 1:
                
                if value != assignment[i, j] and value != 'x' and assignment[i, j] != 'x':
                    return True
                if value == assignment[i, j] == 'x':
                    return True

        return False


        
    def isConsistent(self, var, value, assignment):
        i, j = var
        
        row_count = 0
        col_count = 0

        for x in range(self.N):
            if assignment[x, j] == value:
                col_count += 1

        for y in range(self.M):
            if assignment[i, y] == value:
                row_count += 1

        if value != 'x' and not self.isNeighbor(i, j, value, assignment):
            if value == '+' and row_count < self.row_pos[i] and col_count < self.col_pos[j]:
                return True
            if value == '-' and row_count < self.row_neg[i] and col_count < self.col_neg[j]:
                return True

        elif value == 'x':
            return True

        return False 
                    


    def isNeighbor(self, i, j, pattern, assignment):
        neighbors = [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]
        for neighbor in neighbors:
            if 0 <= neighbor[0] < self.N and 0 <= neighbor[1] < self.M and assignment[neighbor] == pattern:
                return True

        return False


    def get_neighbor(self, var, id):
        i, j = var
        neighbors = [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]
        for neighbor in neighbors:
            if 0 <= neighbor[0] < self.N and 0 <= neighbor[1] < self.M and self.variables[neighbor] == id:
                return neighbor

        return None


    def print(self):
        if not self.board:
            print("No solution")
            return

        for i in range(self.N):
            for j in range(self.M):
                print(self.board[i, j], end=" ")
            print()
        print()
