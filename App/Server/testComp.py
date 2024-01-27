from All_pieces import WCmoves
from UpdateBoard import UpdateBoard
import random
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
    piece = "W"
    current_position = {"x": 0, "y": 1}
    to = {"x":2, "y":3 }
    if board[current_position["y"]][current_position["x"]] != piece:
        print("error")
        return

    W = WCmoves(board, current_position)
    all_posiblekm = W.comp_moves()
    print("all_posiblekm", all_posiblekm)
    uB = UpdateBoard(board)
    to = random.choice(all_posiblekm)
    for m in all_posiblekm:
        if to["to"]["x"] == m["to"]["x"] and to["to"]["y"] == m["to"]["y"]:
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
    movePiece()