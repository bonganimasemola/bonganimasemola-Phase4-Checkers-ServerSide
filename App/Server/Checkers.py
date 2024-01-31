
def makemove(fr, to, board):

    from UpdateBoard import UpdateBoard
    from GameStatus import  white_has_possible_moves, promote,PCMOve
    from All_pieces import Bmoves, KingBMoves,Wmoves, KingWMoves
    from ComputerMove import PCMove
    piece = board[fr['y']][fr['x']]
    if piece == "B" or piece == "KB":
        if piece == "B":
            b = Bmoves(board, co)
            moves= b.moves()
        if piece == 'KB':
            kb = KingBMoves(board, co)
            moves = kb.moves()
        for m in moves:
            if m['to']['x'] == fr['x'] and m['to']['y'] == fr['y']:
                update = UpdateBoard(board)
                newboard = update.move_capture(m)
            else:
                newboard = update.move_only(m)

        white_win = bpm(newboard)
        if white_win == False:
            return{"board":newboard, "win": "BLACK WINS!!"}
        promote = newboard
        pc_move = PCMove(newboard)

        if pc_move == False:
            return {"board":newboard, "win": "b"}
        if pc_move['capture']:
            newboard= update.move_capture(pc_move)
        else:
            newboard = update.move_only(pc_move)

        promote(newboard)