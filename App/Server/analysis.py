rom flask import Flask, jsonify, request
from Moves import Bmoves, Wmoves, KingBMoves, KingWMoves
from UpdateBoard import UpdateBoard
app = Flask(name)
Initialize the game
board = [
    [" ", " ", " ", " ", " ", "W", " ", "W"],
    ["W", " ", "KW", " ", "W", " ", "W", " "],
    [" ", "B", " ", "B", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", "", " "],
    ["B", " ", "B", " ", "B", " ", "B", " "],
    [" ", "B", " ", "KB", " ", "B", " ", "B"],
    ["B", " ", "B", " ", "B", " ", "B", " "],
]
co_kb = {"x": 3, "y": 6}
black_moves = Bmoves(board, co_kb)
white_moves = Wmoves(board, co_kb)
king_black_moves = KingBMoves(board, co_kb)
king_white_moves = KingWMoves(board, co_kb)
update_board = UpdateBoard(board)
@app.route('/api/make_user_move', methods=['POST'])
def make_user_move():
    data = request.get_json()
    user_move = data.get("move")

# Validate the user move
result = play_move(user_move)

# Return the updated game state or an error message
return jsonify({"result": result, "board": update_board.board})
@app.route('/api/make_ai_move', methods=['GET'])
def make_ai_move():

# Implement AI move logic here
ai_move = get_ai_move()

# Validate and play the AI move
result = play_move(ai_move)

# Return the updated game state or an error message
return jsonify({"result": result, "board": update_board.board})
def play_move(move):
    piece = update_board.board[move["from"]["y"]][move["from"]["x"]]
    if piece == "B":
        moves = black_moves
    elif piece == "W":
        moves = white_moves
    elif piece == "KB":
        moves = king_black_moves
    elif piece == "KW":
        moves = king_white_moves
    else:
        return "invalid"

valid_moves = moves.moves()
if move in valid_moves:
    if move.get("capture"):
        update_board.move_capture(move)
    else:
        update_board.move_only(move)

    # Check for win conditions
    if check_win_conditions():
        return "win"

    # Check for draw conditions
    if check_draw_conditions():
        return "draw"

    return "ongoing"
else:
    return "invalid"
def check_win_conditions():

# Define win conditions based on your game rules
# For example, check if the opponent's king is captured
return "KW" not in [piece for row in update_board.board for piece in row]
def check_draw_conditions():

# Define draw conditions based on your game rules
# For example, stalemate or a certain number of moves without captures
return False  # Replace this with your draw conditions
def get_ai_move():

# Implement AI move generation logic here
# This can be a simple algorithm or a more sophisticated AI
# Return the AI-generated move
pass
if name == 'main':
    app.run(debug=True)

