from Player import Player
from Piece import Piece
import os


class Board:
    ROWS_NUM = 9
    COLS_NUM = 9
    map = []
    paired_block_pieces = []

    def __init__(self):
        for y in range(self.ROWS_NUM):
            row = []
            for x in range(self.COLS_NUM):
                state = "empty"
                right_side = "free"
                up_side = "free"
                left_side = "free"
                down_side = "free"
                is_white_goal = False
                is_black_goal = False
                is_border_piece = False
                if y == 0:
                    is_white_goal = True
                    up_side = "block"
                    if x == 4:
                        state = "black"
                elif y == self.ROWS_NUM - 1:
                    is_border_piece = True
                    is_black_goal = True
                    down_side = "block"
                    if x == 4:
                        state = "white"
                if x == 0:
                    left_side = "block"
                elif x == self.COLS_NUM - 1:
                    is_border_piece = True
                    right_side = "block"

                row.append(
                    Piece(
                        x,
                        y,
                        state,
                        right_side,
                        up_side,
                        left_side,
                        down_side,
                        is_white_goal,
                        is_black_goal,
                        is_border_piece,
                    )
                )
            self.map.append(row)

    def get_piece(self, x, y):
        x = min(x, self.COLS_NUM - 1)
        y = min(y, self.ROWS_NUM - 1)
        return self.map[y][x]

    def get_white_goal_pieces(self):
        return self.map[0]

    def get_black_goal_pieces(self):
        return self.map[self.ROWS_NUM - 1]

    def get_piece_neighbors(self, piece: Piece):
        neighbors = []
        x, y = piece.get_position()

        if x + 1 < self.COLS_NUM and piece.r_side != "block":
            neighbors.append(self.get_piece(x + 1, y))
        if y + 1 < self.ROWS_NUM and piece.d_side != "block":
            neighbors.append(self.get_piece(x, y + 1))
        if x - 1 >= 0 and piece.l_side != "block":
            neighbors.append(self.get_piece(x - 1, y))
        if y - 1 >= 0 and piece.u_side != "block":
            neighbors.append(self.get_piece(x, y - 1))

        return neighbors

    def is_reachable(self, white_player: Player, black_player: Player):
        for player in [white_player, black_player]:
            destination = (
                self.get_white_goal_pieces()
                if player.color == "white"
                else self.get_black_goal_pieces()
            )
            visited = {}
            for row in self.map:
                for piece in row:
                    visited[piece] = False

            player_piece = self.get_piece(*player.get_position())

            queue = []
            queue.append(player_piece)
            visited[player_piece] = True
            can_be_reached = False
            while queue:
                piece = queue.pop(0)
                if piece in destination:
                    can_be_reached = True
                    break

                for i in self.get_piece_neighbors(piece):
                    if visited[i] == False:
                        queue.append(i)
                        visited[i] = True

            if not can_be_reached:
                return False

        return True

    def print_map(self):
        VERTICAL_WALL = "\u2503"
        HORIZONTAL_WALL = "\u2501"
        WHITE_PLAYER = "\u265F"
        BLACK_PLAYER = "\u2659"
        SQUARE = "\u00B7"

        os.system("cls" if os.name == "nt" else "clear")

        for y in range(self.ROWS_NUM):
            for x in range(self.COLS_NUM):
                if x == 0:
                    print(VERTICAL_WALL, end=" ")

                piece = self.get_piece(x, y)

                if piece.state == "empty":
                    print(SQUARE, end=" ")
                elif piece.state == "white":
                    print(WHITE_PLAYER, end=" ")
                else:
                    print(BLACK_PLAYER, end=" ")

                if piece.r_side == "block":
                    print(VERTICAL_WALL, end=" ")
                else:
                    print(" ", end=" ")

            print()

            if y != self.ROWS_NUM - 1:
                print(VERTICAL_WALL, end=" ")
                for x in range(self.COLS_NUM):
                    piece = self.get_piece(x, y)
                    if piece.d_side == "block":
                        end_char = (
                            HORIZONTAL_WALL
                            if self.get_piece(x + 1, y).d_side == "block"
                            else " "
                        )
                        print(HORIZONTAL_WALL, end=end_char)
                    # elif self.get_piece(x - 1, y).d_side == "block":
                    #     print(HORIZONTAL_WALL, end=" ")
                    else:
                        print(" ", end=" ")
                    if (
                        piece.r_side == "block"
                        and self.get_piece(x, y + 1).r_side == "block"
                    ):
                        print(VERTICAL_WALL, end=" ")
                    elif (
                        piece.d_side == "block"
                        and self.get_piece(x + 1, y).d_side == "block"
                    ):
                        print(HORIZONTAL_WALL, end=HORIZONTAL_WALL)
                    else:
                        print(" ", end=" ")
                print()

