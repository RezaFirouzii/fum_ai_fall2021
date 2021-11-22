class Piece:
    def __init__(
        self,
        x,
        y,
        state,
        r_side,
        u_side,
        l_side,
        d_side,
        is_white_goal,
        is_black_goal,
        is_border_piece,
    ):
        self.x = x
        self.y = y
        self.state = state
        self.r_side = r_side
        self.u_side = u_side
        self.l_side = l_side
        self.d_side = d_side
        self.is_white_goal = is_white_goal
        self.is_black_goal = is_black_goal
        self.is_border_piece = is_border_piece

    def get_position(self):
        return self.x, self.y
