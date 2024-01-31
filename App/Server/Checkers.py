def makemove(fr, to, board):
    from UpdateBoard import UpdateBoard
    from All_pieces import Bmoves, KingBMoves, Wmoves, KingWMoves

    piece = board[fr['y']][fr['x']]
    update = UpdateBoard(board)

    newboard = board  # Initialize newboard with the original board

    if piece == "B" or piece == "KB":
        if piece == "B":
            b = Bmoves(board, fr)
            moves = b.moves()
            print(moves)
        elif piece == 'KB':
            kb = KingBMoves(board, fr)
            moves = kb.moves()

        for m in moves:
            if m['to']['x'] == to['x'] and m['to']['y'] == to['y']:
                up = UpdateBoard(newboard)
                if m['capture']:
                    newboard = up.move_capture(m)
                else:
                    newboard = up.move_only(m)

    return {"board": newboard}
