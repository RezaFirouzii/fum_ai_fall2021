import numpy as np


def isHorizontallyValid(puzzle, i, j, option):
    if j-1 >= 0 and puzzle[i][j-1] == option[0]:
        return False
    elif i-1 >= 0 and puzzle[i-1][j] == option[0]:
        return False
    elif i-1 >= 0 and puzzle[i-1][j+1] == option[1]:
        return False
    elif j+2 < len(puzzle[0]) and puzzle[i][j+2] == option[1]:
        return False
      
    return True


def isVerticallyValid(puzzle, i, j, option):
    if j-1 >= 0 and puzzle[i][j-1] == option[0]:
        return False
    elif i-1 >= 0 and puzzle[i-1][j] == option[0]:
        return False
    elif j+1 < len(puzzle[0]) and puzzle[i][j+1] == option[0]:
        return False
      
    return True


def isSolved(board):
    rows_pos_count = [0 for _ in range(len(board))]
    rows_neg_count = [0 for _ in range(len(board))]
    for row in range(len(board)):
        for col in range(len(board[0])):
            ch = board[row][col]
            if ch == "+":
                rows_pos_count[row] += 1
            elif ch == "-":
                rows_neg_count[row] += 1
      
      
    cols_pos_count = [0 for _ in range(len(board[0]))]
    cols_neg_count = [0 for _ in range(len(board[0]))]
    for col in range(len(board[0])):
        for row in range(len(board)):
            ch = board[row][col]
            if ch == "+":
                cols_pos_count[col] += 1
            elif ch == "-":
                cols_neg_count[col] += 1
                  
      
    for row in range(len(board)):
        if row_pos[row] != -1:
            if rows_pos_count[row] != row_pos[row]:
                return False
        if row_neg[row] != -1:
            if rows_neg_count[row] != row_neg[row]:
                return False
              
              
      
    for col in range(len(board[0])):
        if col_pos[col] != -1:
            if cols_pos_count[col] != col_pos[col]:
                return False
        if col_neg[col] != -1:
            if cols_neg_count[col] != col_neg[col]:
                return False
        #            
        #  if (col_pos[col] != -1 and rows_pos_count[col] != col_pos[col]) or (col_neg[col] != -1 and rows_neg_count[col] != col_neg[col]) :
        #      return False
      
    return True


def solve(puzzle, i, j):
      
    if i == len(puzzle) and j == 0:
        if isSolved(puzzle):
            print(np.array(puzzle))
            print("\n\n")

    elif j >= len(puzzle[0]):
        solve(puzzle, i+1, 0)
  
    else:           
        if puzzle[i][j] == 0 and puzzle[i][j+1] == 0:
              
            #  option 1 +-
            if isHorizontallyValid(puzzle, i, j, "+-"):
                puzzle[i][j] = "+"
                puzzle[i][j+1] = "-"
                  
                solve(puzzle, i, j+2)
                puzzle[i][j], puzzle[i][j+1] = 0, 0
              
            # option 2 -+
            if isHorizontallyValid(puzzle, i, j, "-+"):
                puzzle[i][j] = "-"
                puzzle[i][j+1] = "+"
                  
                solve(puzzle, i, j+2)
                puzzle[i][j], puzzle[i][j+1] = 0, 0
  
            # option 3 xx
            if True or isHorizontallyValid(puzzle,i,j,"xx"):
                puzzle[i][j] = "x"
                puzzle[i][j+1] = "x"
                  
                solve(puzzle, i, j+2)
                puzzle[i][j], puzzle[i][j+1] = 0, 0
   
        #        vertical check
        elif puzzle[i][j] == 1 and puzzle[i+1][j] == 1:
              
            #        option 1 +-
            if isVerticallyValid(puzzle, i, j, "+-"):
                puzzle[i][j] = "+"
                puzzle[i+1][j] = "-"
                  
                solve(puzzle, i, j+1)
                puzzle[i][j], puzzle[i+1][j] = 0, 0
  
            #        option 2 -+
            if isVerticallyValid(puzzle, i, j, "-+"):
                puzzle[i][j] = "-"
                puzzle[i+1][j] = "+"
                  
                solve(puzzle, i, j+1)
                  
                puzzle[i][j], puzzle[i+1][j] = 1, 1
  
            #        option 3 xx
            if True or isVerticallyValid(puzzle, i, j, "xx"):
                puzzle[i][j] = "x"
                puzzle[i+1][j] = "x"
                  
                solve(puzzle, i, j+1)
                puzzle[i][j], puzzle[i+1][j] = 1, 1

                  
        else:
            solve(puzzle, i, j+1)
  





if __name__ == "__main__":
    puzzle = []

    # Read puzzle
    with open("input/input2_method1.txt", "r") as f:
        f = list(f)
        n, m = map(int, f[0].split())
        row_pos = list(map(int, f[1].split()))
        row_neg = list(map(int, f[2].split()))
        col_pos = list(map(int, f[3].split()))
        col_neg = list(map(int, f[4].split()))

        for row in f[5:]:
            row = list(map(int, row.split()))
            puzzle.append(row)

        solve(puzzle, 0, 0)

    