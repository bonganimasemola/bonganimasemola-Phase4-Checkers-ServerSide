from All_pieces import Bmoves
from UpdateBoard import UpdateBoard

board = [
    [" ", " ", " ", " ", " ", "W", " ", "W"],
    ["W", " ", "W", " ", "W", " ", "W", " "],
    [" ", "B", " ", "W", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", "", " "],
    ["B", " ", "", " ", "W", " ", "B", " "],
    [" ", "B", " ", "B", " ", "B", " ", "B"],
    ["B", " ", "B", " ", "B", " ", "B", " "],
]


def movePiece():
    piece = "B"
    current_position = {"x": 3, "y": 6}
    to = {"x": 5, "y": 4}

    if board[current_position["y"]][current_position["x"]] != piece:
        print("error")
        return

    W = Bmoves(board, current_position)
    all_bm = W.moves()
    print("all_bm", all_bm)
    uB = UpdateBoard(board)

    for m in all_bm:
        # print("Checking move:", m)
        if to["x"] == m["to"]["x"] and to["y"] == m["to"]["y"]:
            print("Moved", m)
            if m.get("capture"):
                new_board = uB.move_capture({
                    "from": current_position,
                    "to": m["to"],
                    "capture": m["capture"]
                })
                print(f"Moved from {current_position} to {m['to']} with capture: {m['capture']}")

                print(F"{new_board} NEW")
                return

if __name__ == '__main__':
    new = movePiece()
    print(new)
