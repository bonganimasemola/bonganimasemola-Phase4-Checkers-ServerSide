from All_pieces import Wmoves, KingWMoves,Bmoves,KingBMoves

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

def black_has_possible_moves(board):
    for r in range(len(board)):
        for c in range(len(board[r])):
            piece = board[r][c]
            if piece == "B" or piece == "KB":
                if piece == "B":
                    BM = Bmoves(board, {"x": c, "y": r})
                    BM_all_moves = BM.moves()
                    if len(BM_all_moves) >= 1:
                        return True
                elif piece == "KB":
                    KB = KingWMoves(board, {"x": c, "y": r})
                    KB_all_moves = KB.moves()
                    if len(KB_all_moves) >= 1:
                        return True
    return False




def promote(board):
    Warr = board[7]
    Barr= board[0]

    for i in range (0, 7):
        WP = Warr[i]
        BP = Barr[i]

        if WP == "W":
           board[7][i] = "KW"
        if BP == "B":
           board[0][i] = "KB"
    return board

def PCMove(board):
    from All_pieces import Wmoves, KingWMoves
    for r in range(0,7):
        for c in range(0,7 ):
            piece = board[r][c]

            if piece == "W":
                w = Wmoves(board,{"x":c, "y":r})
                wmove = w.moves()
                if len(wmove) >= 1:
                    return wmove[0]  
                if piece == "KW":
                    w = KingWMoves(board,{"x":c, "y":r})
                    kmove = w.moves()
                    if len(kmove) >= 1:
                        return kmove[0]
    return False

