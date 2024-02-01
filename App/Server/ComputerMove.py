from All_pieces import Wmoves, KingWMoves
from UpdateBoard import UpdateBoard
import random

def is_within_board(x, y, board):
    return 0 <= x < len(board[0]) and 0 <= y < len(board)

def PCMove(board):
    
    for r in range(len(board)):
        for c in range(len(board[r])):
            piece = board[r][c]
            if piece == "W" or piece == "KW":
                WM = Wmoves(board, {"x": c, "y": r})
                KW = KingWMoves(board, {"x": c, "y": r})
                WM_all_moves = WM.moves()
                KW_all_moves = KW.moves()
                
                capture_moves_wm = [move for move in WM_all_moves if move.get("capture") and is_within_board(move["to"]["x"], move["to"]["y"], board)]
                regular_moves_wm = [move for move in WM_all_moves if not move.get("capture") and is_within_board(move["to"]["x"], move["to"]["y"], board)]

                capture_moves_kw = [move for move in KW_all_moves if move.get("capture") and is_within_board(move["to"]["x"], move["to"]["y"], board)]
                regular_moves_kw = [move for move in KW_all_moves if not move.get("capture") and is_within_board(move["to"]["x"], move["to"]["y"], board)]
                
                if capture_moves_wm or capture_moves_kw:
                   
                    all_capture_moves = capture_moves_wm + capture_moves_kw
                    computer_move = random.choice(all_capture_moves)
                    update_board = UpdateBoard(board)
                    board = update_board.move_capture(computer_move)
                    return computer_move, board
                elif regular_moves_wm or regular_moves_kw:
                   
                    all_regular_moves = regular_moves_wm + regular_moves_kw
                    computer_move = random.choice(all_regular_moves)
                    update_board = UpdateBoard(board)
                    board = update_board.move_only(computer_move)
                    return computer_move, board
    
    return None, board  

