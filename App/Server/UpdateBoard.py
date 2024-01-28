class UpdateBoard:
    def __init__(self, board):
        self.board = [row[:] for row in board]

    def valid_moves(self, arr):
        if isinstance(arr, list):
            for m in arr:
                to = m["to"]
                self.board[to["y"]][to["x"]] = "X"
            print(self.board)
            return self.board

    def move_capture(self, move_data):
        piece = self.board[move_data["from"]["y"]][move_data["from"]["x"]]
        self.board[move_data["to"]["y"]][move_data["to"]["x"]] = piece
        self.board[move_data["from"]["y"]][move_data["from"]["x"]] = ""
        self.board[move_data["capture"]["y"]][move_data["capture"]["x"]] = ""
        return self.board

    def move_only(self, move_data):
        piece = self.board[move_data["from"]["y"]][move_data["from"]["x"]]
        self.board[move_data["to"]["y"]][move_data["to"]["x"]] = piece
        self.board[move_data["from"]["y"]][move_data["from"]["x"]] = ""
        return self.board

    def analyze_board(self):
        for row_index, row in enumerate(self.board):
            for i in range(len(row)):
                piece = row[i]
                if piece == "B":
                    self.board[row_index][i] = "KB"
                elif piece == "W":
                    self.board[row_index][i] = "KW"
                else:
                    print("Invalid Coordinates")
