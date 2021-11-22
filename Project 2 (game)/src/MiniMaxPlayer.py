from Player import Player
from copy import deepcopy


class MiniMaxPlayer(Player):
    MAX_DEPTH = 2
    INFINITY = 9999
    transposition_table = {}

    # finds the shortest path from the current position to either the goal or next row
    def bfs(self, opponent: Player, goal=False):
        for player in [self, opponent]:

            row = player.get_position()[1] - 1 if player.color == "white" else player.get_position()[1] + 1
            row = max(0, row)
            row = min(8, row)
            destination = self.board.map[row]
            
            if goal:
                destination = (
                    self.board.get_white_goal_pieces()
                    if player.color == "white"
                    else self.board.get_black_goal_pieces()
                )

            visited = {}
            distances = {}
            for row in self.board.map:
                for piece in row:
                    visited[piece] = False
                    distances[piece] = self.INFINITY

            player_piece = self.board.get_piece(*player.get_position())

            queue = []
            queue.append(player_piece)
            visited[player_piece] = True
            distances[player_piece] = 0

            while queue:
                piece = queue.pop(0)

                for i in self.board.get_piece_neighbors(piece):
                    if visited[i] == False:
                        distances[i] = distances[piece] + 1
                        visited[i] = True
                        queue.append(i)

            min_distance = self.INFINITY
            for piece, dist in distances.items():
                if piece in destination:
                    if dist < min_distance:
                        min_distance = dist

            if player == self:
                self_distance = min_distance
            else:
                opponent_distance = min_distance

        return self_distance, opponent_distance

    # evaluates the current state of the game
    def evaluate(self, opponent):
        self_distance, opponent_distance = self.bfs(opponent, goal=True)
        self_row_distance, opponent_row_distance = self.bfs(opponent)

        # features
        f1 = opponent_distance - self_distance  # difference in distance to goal
        f2 = opponent_row_distance - self_row_distance # difference in distance to next row
        f3 = abs(self.init_row - self.get_position()[1]) - self_distance # difference in rows progression number and distance to goal 
        f4 = opponent.walls_count - self.walls_count    # difference in walls count
        # weights
        w1 = self.walls_count // 2
        w2 = self.walls_count // 2
        w3 = 1
        w4 = 1
        return f1*w1 + f2*w2 + f3*w3 + f4*w4

    ############################ minimax algorithm ############################
    def minimax(self, depth, is_max_player, opponent):
        if depth == 0:
            return self.evaluate(opponent)

        if is_max_player:
            best_value = -self.INFINITY
            for action in self.get_legal_actions(opponent):
                self.play(action, is_evaluating=True)
                best_value = max(best_value, opponent.minimax(depth - 1, False, self))
                self.undo_last_action()
            return best_value
        else:
            best_value = self.INFINITY
            for action in self.get_legal_actions(opponent):
                self.play(action, is_evaluating=True)
                best_value = min(best_value, opponent.minimax(depth - 1, True, self))
                self.undo_last_action()
            return best_value


    ############################ alpha-beta pruning algorithm ############################
    def alpha_beta_search(self, depth, alpha, beta, is_max_player, opponent):
        if depth == 0:
            return self.evaluate(opponent)

        if is_max_player:
            best_value = -self.INFINITY
            for action in self.get_legal_actions(opponent):
                self.play(action, is_evaluating=True)
                best_value = max(best_value, opponent.alpha_beta_search(depth - 1, alpha, beta, False, self))
                self.undo_last_action()
                alpha = max(alpha, best_value)
                if beta <= alpha:
                    break
            return best_value
        else:
            best_value = self.INFINITY
            for action in self.get_legal_actions(opponent):
                self.play(action, is_evaluating=True)
                best_value = min(best_value, opponent.alpha_beta_search(depth - 1, alpha, beta, True, self))
                self.undo_last_action()
                beta = min(beta, best_value)
                if beta <= alpha:
                    break
            return best_value

        
    # alpha-beta pruning algorithm with Transposition Table
    def alpha_beta_TT(self, depth, alpha, beta, is_max_player, opponent):

        current_key = self.hash(is_max_player, depth)
        if current_key in self.transposition_table.keys() and depth == self.transposition_table[current_key].depth:
            return self.transposition_table[current_key].value

        if depth == 0:
            score = self.evaluate(opponent)
            self.transposition_table[current_key] = TTEntry(score, depth)
            return score

        if is_max_player:
            best_value = -self.INFINITY
            for action in self.get_legal_actions(opponent):
                self.play(action, is_evaluating=True)
                best_value = max(best_value, opponent.alpha_beta_TT(depth - 1, alpha, beta, False, self))
                self.undo_last_action()
                alpha = max(alpha, best_value)
                if beta <= alpha:
                    break
            self.transposition_table[current_key] = TTEntry(best_value, depth)
            return best_value
        else:
            best_value = self.INFINITY
            for action in self.get_legal_actions(opponent):
                self.play(action, is_evaluating=True)
                best_value = min(best_value, opponent.alpha_beta_TT(depth - 1, alpha, beta, True, self))
                self.undo_last_action()
                beta = min(beta, best_value)
                if beta <= alpha:
                    break
            self.transposition_table[current_key] = TTEntry(best_value, depth)
            return best_value


    # maps the board state to a unique string
    def hash(self, is_max_player, depth):
        key = f"{depth}-{is_max_player}-"
        for row in self.board.map:
            for piece in row:
                key += f'{piece.x}-{piece.y}-{piece.state}-\
                {piece.r_side}-{piece.u_side}-{piece.l_side}-{piece.d_side}-\
                {piece.is_white_goal}-{piece.is_black_goal}-{piece.is_border_piece}'
        
        return key


    def get_best_action(self, opponent):
        best_action = None
        best_value = -self.INFINITY
        for action in self.get_legal_actions(opponent):
            self.play(action, is_evaluating=True)
            # value = opponent.minimax(self.MAX_DEPTH, False, self)
            # value = opponent.alpha_beta_search(self.MAX_DEPTH - 1, -self.INFINITY, self.INFINITY, False, self)
            value = opponent.alpha_beta_TT(self.MAX_DEPTH - 1, -self.INFINITY, self.INFINITY, False, self)
            self.undo_last_action()
            if value > best_value:
                best_value = value
                best_action = action

        return best_action


        

class TTEntry:
    def __init__(self, value, depth):
        self.value = value
        self.depth = depth