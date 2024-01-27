class Moves:
    """Represents possible moves for a checker piece."""
    capture_piece = {
        "W": ["B", "KB"],
        "B": ["W", "KW"],
        "KW": ["B", "KB"],
        "KB": ["W", "KW"],
    }

    def __init__(self, board, all_moves, piece, co):
        """Initializes the Moves object with a copy of the board."""
        self.board = [row[:] for row in board]
        self.all_moves = all_moves
        self.piece = piece
        self.to_capture = Moves.capture_piece.get(piece, None).copy()
        self.co = co

    def moves(self):
        print("Calculating moves for", self.piece)
        all_moves = []

        if self.board[self.co["y"]][self.co["x"]] != self.piece:
            print("Piece not found at", self.co)
            return all_moves

        for move in self.all_moves:
            to = move["to"]
            capture = move.get("capture")

            y_move = to["y"] + self.co["y"]
            x_move = to["x"] + self.co["x"]

            if 0 <= x_move < 8 and 0 <= y_move < 8:
                move_position = self.board[y_move][x_move].strip()

                print("Checking move:", move, "to:", {"x": x_move, "y": y_move}, "position:", move_position)  # Debugging

                if move_position == "":  # Update this line
                    position = {
                        "from": {"x": self.co["x"], "y": self.co["y"]},
                        "to": {"x": x_move, "y": y_move},
                    }

                    if capture:
                        result = self.handle_capture(capture, x_move, y_move)
                        if result:
                            position["capture"] = result
                            all_moves.append(position)
                            continue

                    all_moves.append({**position, "capture": False})
                else:
                    print("Position not empty. Current state:", self.board)

            else:
                print("Move out of board range:", move, "to:", {"x": x_move, "y": y_move})

        return all_moves

    def handle_capture(self, capture, x_move, y_move):
        if not self.to_capture:
            return None

        x, y = capture
        cap_x, cap_y = x_move + capture["x"], y_move + capture["y"]


        if 0 <= cap_x < 8 and 0 <= cap_y < 8:
            capture_position = self.board[cap_y][cap_x].strip()

            if capture_position in self.to_capture:
                return {"x": cap_x, "y": cap_y}

        return None
    
    