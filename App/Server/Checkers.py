def makemove(fr, to, board):
    from UpdateBoard import UpdateBoard
    from All_pieces import Bmoves, KingBMoves, Wmoves, KingWMoves

    piece = board[fr['y']][fr['x']]

    newboard = board  # Initialize newboard with the original board

    if piece == "B" or piece == "KB":
        if piece == "B":
            b = Bmoves(board, fr)
            moves = b.moves()
            print("B moves:", moves)
        elif piece == 'KB':
            kb = KingBMoves(board, fr)
            moves = kb.moves()
            print("KB moves:", moves)

        for m in moves:
            if 'to' in m:
                to_coords = m['to']
                if 'x' in to_coords and 'y' in to_coords and 'x' in to and 'y' in to:
                    if to_coords['x'] == to['x'] and to_coords['y'] == to['y']:
                        # Directly use UpdateBoard without the unused update variable
                        if m['capture']:
                            newboard = UpdateBoard(newboard).move_capture(m)
                        else:
                            newboard = UpdateBoard(newboard).move_only(m)

    return {"board": newboard}
