class Player:
    def __init__(self, color, x, y, board):
        self.color = color
        self.x = x
        self.y = y
        self.init_row = y
        self.walls_count = 10
        self.board = board
        self.actions_logs = []
        self.moves_count = 0

    def get_position(self):
        return self.x, self.y

    def move(self, x, y):
        self.board.get_piece(self.x, self.y).state = "empty"

        self.x = x
        self.y = y

        self.board.get_piece(self.x, self.y).state = self.color

    def put_wall(self, x, y, orientation):
        """
        The wall will be put right/down side 
        of the piece with X and Y position and 
        its neighbor
        """

        self.walls_count -= 1

        piece = self.board.get_piece(x, y)
        if orientation == "horizontal":
            neighbor_piece1 = self.board.get_piece(x + 1, y)
            neighbor_piece2 = self.board.get_piece(x, y + 1)
            neighbor_piece3 = self.board.get_piece(x + 1, y + 1)
            piece.d_side = "block"
            neighbor_piece1.d_side = "block"
            neighbor_piece2.u_side = "block"
            neighbor_piece3.u_side = "block"
            self.board.paired_block_pieces.append((piece, neighbor_piece1))
        elif orientation == "vertical":
            neighbor_piece1 = self.board.get_piece(x, y + 1)
            neighbor_piece2 = self.board.get_piece(x + 1, y)
            neighbor_piece3 = self.board.get_piece(x + 1, y + 1)
            piece.r_side = "block"
            neighbor_piece1.r_side = "block"
            neighbor_piece2.l_side = "block"
            neighbor_piece3.l_side = "block"
            self.board.paired_block_pieces.append((piece, neighbor_piece1))

    def play(self, command, is_evaluating=False):
        if not is_evaluating:
            self.moves_count += 1
        splitted_command = command.split("#")

        if splitted_command[0] == "move":
            x = int(splitted_command[1])
            y = int(splitted_command[2])
            self.actions_logs.append(f"move#{self.x}#{self.y}#{x}#{y}")
            self.move(x, y)
        else:
            x = int(splitted_command[1])
            y = int(splitted_command[2])
            orientation = splitted_command[3]
            self.actions_logs.append(command)
            self.put_wall(x, y, orientation)

    def undo_last_action(self):
        last_action = self.actions_logs.pop()
        splitted_command = last_action.split("#")

        if splitted_command[0] == "wall":
            self.remove_wall(last_action)
        else:
            x = int(splitted_command[1])
            y = int(splitted_command[2])
            self.move(x, y)

    def remove_wall(self, command: str):
        """
        The wall will be removed from right/down side 
        of the piece with X and Y position and 
        its neighbor

        the format of command is like:
            wall#X#Y#ORIENTATION
        """

        self.walls_count += 1

        splitted_command = command.split("#")
        x = int(splitted_command[1])
        y = int(splitted_command[2])
        orientation = splitted_command[3]

        piece = self.board.get_piece(x, y)
        if orientation == "horizontal":
            neighbor_piece1 = self.board.get_piece(x + 1, y)
            neighbor_piece2 = self.board.get_piece(x, y + 1)
            neighbor_piece3 = self.board.get_piece(x + 1, y + 1)
            piece.d_side = "free"
            neighbor_piece1.d_side = "free"
            neighbor_piece2.u_side = "free"
            neighbor_piece3.u_side = "free"
            self.board.paired_block_pieces.remove((piece, neighbor_piece1))
        elif orientation == "vertical":
            neighbor_piece1 = self.board.get_piece(x, y + 1)
            neighbor_piece2 = self.board.get_piece(x + 1, y)
            neighbor_piece3 = self.board.get_piece(x + 1, y + 1)
            piece.r_side = "free"
            neighbor_piece1.r_side = "free"
            neighbor_piece2.l_side = "free"
            neighbor_piece3.l_side = "free"
            self.board.paired_block_pieces.remove((piece, neighbor_piece1))

    def is_winner(self):
        player_piece = self.board.get_piece(*self.get_position())

        if self.color == "white":
            if player_piece in self.board.get_white_goal_pieces():
                return True

        if self.color == "black":
            if player_piece in self.board.get_black_goal_pieces():
                return True

        return False

    def can_place_wall(self, piece, orientation):
        if self.walls_count > 0:
            x, y = piece.get_position()
            if not piece.is_border_piece:
                if orientation == "horizontal":
                    if (
                        piece.d_side == "free"
                        and self.board.get_piece(x + 1, y).d_side == "free"
                    ):
                        if (
                            piece,
                            self.board.get_piece(x, y + 1),
                        ) not in self.board.paired_block_pieces:
                            return True

                if orientation == "vertical":
                    if (
                        piece.r_side == "free"
                        and self.board.get_piece(x, y + 1).r_side == "free"
                    ):
                        if (
                            piece,
                            self.board.get_piece(x + 1, y),
                        ) not in self.board.paired_block_pieces:
                            return True

        return False

    def get_legal_actions(self, opponent):
        player_piece = self.board.get_piece(self.x, self.y)
        opponent_piece = self.board.get_piece(opponent.x, opponent.y)

        legal_moves = []

        # move right
        if player_piece.r_side != "block":
            if opponent_piece.get_position() != (self.x + 1, self.y):
                legal_moves.append(f"move#{self.x+1}#{self.y}")
            else:  # Opponent is present
                if opponent_piece.r_side == "free":
                    legal_moves.append(f"move#{self.x+2}#{self.y}")
                else:
                    if opponent_piece.u_side == "free":
                        legal_moves.append(f"move#{self.x+1}#{self.y-1}")
                    if opponent_piece.d_side == "free":
                        legal_moves.append(f"move#{self.x+1}#{self.y+1}")

        # move down
        if player_piece.d_side != "block":
            if opponent_piece.get_position() != (self.x, self.y + 1):
                legal_moves.append(f"move#{self.x}#{self.y+1}")
            else:  # Opponent is present
                if opponent_piece.d_side == "free":
                    legal_moves.append(f"move#{self.x}#{self.y+2}")
                else:
                    if opponent_piece.r_side == "free":
                        legal_moves.append(f"move#{self.x+1}#{self.y+1}")
                    if opponent_piece.l_side == "free":
                        legal_moves.append(f"move#{self.x-1}#{self.y+1}")

        # move left
        if player_piece.l_side != "block":
            if opponent_piece.get_position() != (self.x - 1, self.y):
                legal_moves.append(f"move#{self.x-1}#{self.y}")
            else:  # Opponent is present
                if opponent_piece.l_side == "free":
                    legal_moves.append(f"move#{self.x-2}#{self.y}")
                else:
                    if opponent_piece.u_side == "free":
                        legal_moves.append(f"move#{self.x-1}#{self.y-1}")
                    if opponent_piece.d_side == "free":
                        legal_moves.append(f"move#{self.x-1}#{self.y+1}")

        # move up
        if player_piece.u_side != "block":
            if opponent_piece.get_position() != (self.x, self.y - 1):
                legal_moves.append(f"move#{self.x}#{self.y-1}")
            else:  # Opponent is present
                if opponent_piece.u_side == "free":
                    legal_moves.append(f"move#{self.x}#{self.y-2}")
                else:
                    if opponent_piece.l_side == "free":
                        legal_moves.append(f"move#{self.x-1}#{self.y-1}")
                    if opponent_piece.r_side == "free":
                        legal_moves.append(f"move#{self.x+1}#{self.y-1}")

        # PUT WALL
        for row in self.board.map:
            for piece in row:
                for orientation in ["vertical", "horizontal"]:
                    if self.can_place_wall(piece, orientation):
                        command = f"wall#{piece.x}#{piece.y}#{orientation}"
                        self.put_wall(piece.x, piece.y, orientation)
                        if self.board.is_reachable(self, opponent):
                            legal_moves.append(command)
                        self.remove_wall(command)

        return legal_moves
