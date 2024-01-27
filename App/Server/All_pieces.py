from Moves import Moves
from ComputerMove import Opponent

class Bmoves(Moves):
    def __init__(self, board, co):
        Black_moves = [
            {"to": {"x": 1, "y": -1}, "capture": False},
            {"to": {"x": -1, "y": -1}, "capture": False},
            {"to": {"x": 2, "y": -2}, "capture": {"x": -1, "y": 1}},
            {"to": {"x": -2, "y": -2}, "capture": {"x": 1, "y": 1}},
        ]
        
        Black_moves.append({"to": co, "capture": False})
        super().__init__(board, all_moves = Black_moves, piece="B", co=co)
        
    def initialize_moves(self):
        print("Calculating moves for  W")
        # Remove the next line to prevent re-initialization
        # self.all_kwm = self.moves()

    def display_moves(self):
        print("W Moves:", self.all_bm)


class Wmoves(Moves):
    def __init__(self, board, co):
        white_moves = [
            {"to": {"x": 1, "y": 1}, "capture": False},
            {"to": {"x": -1, "y": 1}, "capture": False},
            {"to": {"x": 2, "y": 2}, "capture": {"x": -1, "y": -1}},
            {"to": {"x": -2, "y": 2}, "capture": {"x": 1, "y": -1}},
        ]
        
        white_moves.append({"to": co, "capture": False})
        super().__init__(board, all_moves=white_moves, piece="W", co=co)
        
    def initialize_moves(self):
        print("Calculating moves for  W")
        # Remove the next line to prevent re-initialization
        # self.all_kwm = self.moves()

    def display_moves(self):
        print("W Moves:", self.all_wm)



class KingWMoves(Moves):
    """Represents possible moves for a white king."""

    def __init__(self, board, co):
        moves = [
            {"to": {"x": 1, "y": 1}, "capture": False},
            {"to": {"x": -1, "y": 1}, "capture": False},
            {"to": {"x": 1, "y": -1}, "capture": False},
            {"to": {"x": -1, "y": -1}, "capture": False},
            {"to": {"x": 2, "y": 2}, "capture": {"x": -1, "y": -1}},
            {"to": {"x": -2, "y": 2}, "capture": {"x": 1, "y": -1}},
            {"to": {"x": 2, "y": 1}, "capture": False},
        ]
        super().__init__(board, moves, "KW", co)
        self.initialize_moves() 

    def initialize_moves(self):
        print("Calculating moves for King W")
        # Remove the next line to prevent re-initialization
        # self.all_kwm = self.moves()

    def display_moves(self):
        print("King W Moves:", self.all_kwm)





class KingBMoves(Moves):
    def __init__(self, board, co):
        # print("Initializing KingBMoves with coordinates:", co)
        king_b_moves = [
            {"to": {"x": 1, "y": 1}, "capture": False},
            {"to": {"x": -1, "y": 1}, "capture": False},
            {"to": {"x": 1, "y": -1}, "capture": False},
            {"to": {"x": -1, "y": -1}, "capture": False},
            {"to": {"x": 2, "y": 2}, "capture": {"x": -1, "y": -1}},
            {"to": {"x": -2, "y": 2}, "capture": {"x": 1, "y": -1}},
            {"to": {"x": 2, "y": -2}, "capture": {"x": -1, "y": 1}},
            {"to": {"x": -2, "y": -2}, "capture": {"x": 1, "y": 1}},
        ]
        
        king_b_moves.append({"to": co, "capture": False})
        super().__init__(board, all_moves=king_b_moves, piece="KB", co=co)
        
    def initialize_moves(self):
        print("Calculating moves for King W")
        # Remove the next line to prevent re-initialization
        # self.all_kwm = self.moves()

    def display_moves(self):
        print("King W Moves:", self.all_kbm)
