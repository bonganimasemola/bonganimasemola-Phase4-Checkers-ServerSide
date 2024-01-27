from All_pieces import Wmoves, KingWMoves

class GameLogic:
    def __init__(self, board):
        self.board = board
def white_has_possible_moves(board):
    for r in range(len(board)):
        for c in range(len(board[r])):
            piece = board[r][c]
            if piece == "W" or piece == "KW":
                if piece == "W":
                    WM = Wmoves(board, {"x": c, "y": r})
                    WM_all_moves = WM.moves()
                    if len(WM_all_moves) >= 1:
                        return True
                elif piece == "KW":
                    KW = KingWMoves(board, {"x": c, "y": r})
                    KW_all_moves = KW.moves()
                    if len(KW_all_moves) >= 1:
                        return True
    return False

