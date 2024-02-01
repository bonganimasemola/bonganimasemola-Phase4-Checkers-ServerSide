def makemove(fr, to, board):
    from UpdateBoard import UpdateBoard
    from All_pieces import Bmoves, KingBMoves, Wmoves, KingWMoves
    from GameStatus import white_has_possible_moves, promote, PCMove, black_has_possible_moves

    piece = board[fr['y']][fr['x']]
    
    new_board = board  # Initialize new_board with the original board

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
                            new_board = UpdateBoard(new_board).move_capture(m)
                        else:
                            new_board = UpdateBoard(new_board).move_only(m)

    black_w = white_has_possible_moves(new_board)
    if black_w == False:
        return {"board": new_board, "win": "b won"}
    #promote(new_board)

    # white_w = white_has_possible_moves(new_board)
    # if white_w == False:
    #     return {"board": new_board, "win": "b"}

    promote(new_board)

    pc_m = PCMove(new_board)
    if pc_m == False:
        return {"board": new_board, "win": "b"}
    if pc_m == ['capture']:
        new_board = UpdateBoard(new_board).move_capture(pc_m)
    else:
        new_board = UpdateBoard(new_board).move_only(pc_m)
    
    promote(new_board)

    white_w = black_has_possible_moves(new_board)

    if white_w == False:
        return {"board": new_board, "win": "w"}
    
    return {"board": new_board, "win": "False"}

    # The following line is unreachable due to the return statement above
    # return {"error": True, "message": "invalid"}
