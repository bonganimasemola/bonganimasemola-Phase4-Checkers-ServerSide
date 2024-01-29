from flask import Flask, redirect, url_for, request, jsonify, render_template
from datetime import datetime
from GameStatus import GameLogic
# from UpdateBoard import UpdateBoard
# from Moves import Moves
# from All_pieces import Bmoves, KingBMoves, Wmoves, KingWMoves
from flask_cors import CORS
from models import db, Player, Game, Move, Piece
from werkzeug.security import check_password_hash
import json
from flask_login import LoginManager,login_user, login_required, logout_user, current_user, UserMixin
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate



app = Flask(__name__, template_folder='/Users/bonganimasemola/Development/coding/PHASE4/bonganimasemola-Phase4-Checkers-ServerSide/App/Server/templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  
app.config['SECRET_KEY'] = 'your_secret_key'
CORS(app)

db.init_app(app)
# db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

#mock up User class for testing
class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id
        



with app.app_context():
    db.create_all()
    
original_board = [
    [" ", "W", " ", "W", " ", "W", " ", "W"],
    ["W", " ", "W", " ", "W", " ", "W", " "],
    [" ", "W", " ", "W", " ", "W", " ", "W"],
    [" ", " ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", " ", " "],
    ["B", " ", "B", " ", "B", " ", "B", " "],
    [" ", "B", " ", "B", " ", "B", " ", "B"],
    ["B", " ", "B", " ", "B", " ", "B", " "],
]

def get_opponent_id(user_id):
    game = Game.query.filter_by(winner_id=None).filter_by(is_draw=False).filter(Game.player_id != user_id).first()
    if game:
        return game.player_id
    return None
    
    
# FRONT-END FACING ROUTES:
@app.route('/')
def home():
    data = {'Server side': 'Checkers'}
    return jsonify(data), 200

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = Player.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Login failed. Check your username and password.')
    return render_template('login.html')


@app.route('/dashboard')
@login_required
def dashboard():
    return f'Hello, {current_user.username}! You are now logged in.'

@app.route('/players', methods=['GET'])
def get_players():
    players = Player.query.all()
    player_list = [{'id': player.id, 'username': player.username} for player in players]
    return jsonify(player_list), 200

@app.route('/players/<int:player_id>', methods=['GET'])
def get_player_by_id(player_id):
    player = Player.query.get(player_id)

    if player:
        return jsonify({'id': player.id, 'username': player.username}), 200
    else:
        return jsonify({'error': 'Player not found'}), 404

@app.route('/players', methods=['POST'])
def create_player():
    data = request.get_json()
    try:
        if 'username' in data and 'email' in data and 'password' in data:
            new_player = Player(username=data['username'], email=data['email'])
            new_player.set_password(data['password'])
            db.session.add(new_player)
            db.session.commit()
            return jsonify({"username": new_player.username, "email": new_player.email}), 201
        else:
            return jsonify({'message': 'Missing username, email, or password in the request'}), 400
    except Exception as e:
        print(f"Error creating player: {e}")
        db.session.rollback()
        return jsonify({'message': 'Error creating player'}), 500
    


@app.route('/logout')
@login_required
def logout():
    if current_user.is_authenticated:
        logout_user()
    return redirect(url_for('login'))


# BACK-END FACING ROUTES:
@app.route('/start_game', methods=['POST'])
@login_required
def start_game():
    # user_id = Player.id  # Uncomment this line if using Flask-Login
    user_id = 1  # Replace with your actual way of getting user id

    original_board = request.json.get('board', None)

    if not original_board:
        # Create a new game with the user as the winner (assuming the game is won by someone)
        game = Game(date_started=datetime.utcnow(), winner_id=user_id)
        db.session.add(game)
        db.session.commit()

        return jsonify({"message": "Game started successfully.", "game_id": game.id}), 200
    else:
        # Return the board from the existing game
        return jsonify({"message": "Existing game retrieved successfully.", "board": original_board}), 200

@app.route('/forfeit_game/<int:game_id>', methods=['POST'])
@login_required
def forfeit_game(game_id):
    user_id = current_user.id

    game = Game.query.get(game_id)
    
    if game is None:
        return jsonify({"error": "Game not found."}), 404

    if game.player_id != user_id:
        return jsonify({"error": "You are not authorized to forfeit this game."}), 403

    # Update the game with a loss
    gameLogic = GameLogic(game.board)
    gameLogic.update_game_loss()
    game.date_finished = datetime.utcnow()
    game.winner_id = get_opponent_id(user_id)
    game.is_draw = False
    db.session.commit()

    return jsonify({"message": "Game forfeited successfully.", "winner_id": game.winner_id}), 200

@app.route('/games', methods=['POST'])
def create_game():
    data = request.get_json()

    # Check if 'board' key is present in the JSON data
    if 'board' not in data:
        return jsonify({'error': 'Missing "board" key in JSON data'}), 400

    initial_board = data['board']

    # Validate that 'board' is a list of lists (2D list)
    if not isinstance(initial_board, list) or not all(isinstance(row, list) for row in initial_board):
        return jsonify({'error': 'Invalid format for "board" data'}), 400

    # Create a new game
    new_game = Game(board=initial_board)
    
    try:
        db.session.add(new_game)
        db.session.commit()
        return jsonify({'message': 'Game created successfully', 'game_id': new_game.id}), 201
    except Exception as e:
        # Handle database errors
        db.session.rollback()
        return jsonify({'error': 'Failed to create game', 'details': str(e)}), 500
    finally:
        db.session.close()

@app.route('/games/<int:game_id>', methods=['GET'])
def get_game(game_id):
    game = Game.query.get(game_id)
    if not game:
        return jsonify({'error': 'Game not found'}), 404

    return jsonify({
        'message': 'Game retrieved successfully',
        'game_id': game.id,
        'board': game.board,
    }), 200


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data['name']
    email = data['email']
    password = data['password']

    # Check for existing user with the same email
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({'error': 'User already exists'}), 400

    # Create a new user
    new_user = User(name=name, email=email, password=password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User created successfully'}), 201


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data['email']
    password = data['password']

    user = User.query.filter_by(email=email).first()
    if user and user.password == password:
        # Create a session token or similar for authentication
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'error': 'Invalid email or password'}), 401


@app.route('/games/<int:game_id>/move', methods=['POST'])
def make_move(game_id):
    data = request.get_json()
    move = data['move']  

    game = Game.query.get(game_id)
    if not game:
        return jsonify({'error': 'Game not found'}), 404

    # Get the current board state
    current_board = game.board

    # Validate the move and get the updated board
    updated_board, promotion = validate_and_make_move(current_board, move)

    if updated_board:
        # Update the game's board
        game.board = updated_board

        # Check for promotions
        if promotion:
            handle_promotion(updated_board, promotion)

        # Save the updated game state to the database
        db.session.commit()

        return jsonify({'message': 'Move successful', 'updated_board': updated_board})
    else:
        return jsonify({'error': 'Invalid move'}), 400


def validate_and_make_move(current_board, move):
    # Assuming your classes are imported properly
    piece = current_board[move["from"]["y"]][move["from"]["x"]]

    # Validate the move based on the piece type (W, KW, B, KB)
    if piece == "W" :
        moves_instance = Wmoves(current_board, move["from"])
    elif  piece == "KW":
        moves_instance = KingWMoves(current_board, move["from"])
    elif piece == "KB":
        moves_instance = KingBMoves(current_board, move["from"])
    elif piece == "B": 
        moves_instance = Bmoves(current_board, move["from"])
    else:
        return None, None  # Invalid piece type

    all_moves = moves_instance.moves()

    # Check if the move is in the list of valid moves
    if move in all_moves:
        updated_board = update_board(current_board, move)
        promotion = check_for_promotion(updated_board, move)
        return updated_board, promotion
    else:
        return None, None  # Invalid move


def update_board(board, move):
    
    update_board_instance = UpdateBoard(board)
    updated_board = update_board_instance.move_capture(move)  # Assuming move is a capture move
    return updated_board


def check_for_promotion(board, move):
    co = move["to"]  # Assuming the coordinates are in "to" key
    piece = board[co["y"]][co["x"]]

    if piece == "W" and co["y"] == 7:
        return "KW"
    elif piece == "B" and co["y"] == 0:
        return "KB"
    else:
        return None


def handle_promotion(board, promotion, move):
   
    co = move["to"]  # Assuming the coordinates are in "to" key

    if promotion == "KW":
        board[co["y"]][co["x"]] = "KW"
    elif promotion == "KB":
        board[co["y"]][co["x"]] = "KB"
        
    
        
# Update the board accordingly
# # Update the game with a loss
# gameLogic = GameLogic(game.board)
# gameLogic.update_game_loss()
# game.date_finished = datetime.utcnow()
# game.winner_id = get_opponent_id(user_id)
# game.is_draw = False
# db.session.commit()

# return jsonify({"message": "Game forfeited successfully.", "winner_id": game.winner_id}), 200
# @app.route('/get_valid_moves', methods=['POST'])
# @login_required
# def get_valid_moves():
#     user_id = current_user.id
#     game_id = request.json.get('game_id', None)
#     piece = request.json.get('piece', None)

# if not game_id or not piece:
#     return jsonify({"error": "Game ID and piece are required parameters."}), 400

# game = Game.query.get(game_id)
# if game is None:
#     return jsonify({"error": "Game not found."}), 404

# if game.player_id != user_id:
#     return jsonify({"error": "You are not authorized to get moves for this game."}), 403

# # Convert the board to object
# board_object = [list(row) for row in game.board.split('\n')]

# # Check if the piece exists
# piece_exists = False
# for row in board_object:
#     if piece in row:
#         piece_exists = True
#         break

# if not piece_exists:
#     return jsonify({"error": "Piece not found on the board."}), 400

# # Call getBmoves, getKwMoves
# if piece == "W":
#     wm = Wmoves(board_object, {"x": 0, "y": 0})
#     wm_all_moves = wm.moves()
#     return jsonify({"valid_moves": wm_all_moves}), 200
# elif piece == "KW":
#     kw = KingWMoves(board_object, {"x": 0, "y": 0})
#     kw_all_moves = kw.moves()
#     return jsonify({"valid_moves": kw_all_moves}), 200
# else:
#     return jsonify({"error": "Invalid piece type."}), 400
# @app.route('/make_move', methods=['POST'])
# @login_required
# def make_move():
#     user_id = current_user.id
#     game_id = request.json.get('game_id', None)
#     move_data = request.json.get('move_data', None)

# if not game_id or not move_data:
#     return jsonify({"error": "Game ID and move data are required parameters."}), 400

# game = Game.query.get(game_id)
# if game is None:
#     return jsonify({"error": "Game not found."}), 404

# if game.player_id != user_id:
#     return jsonify({"error": "You are not authorized to make a move for this game."}), 403

# # Convert the board to object
# board_object = [list(row) for row in game.board.split('\n')]

# # Check if the piece exists
# piece_exists = False
# for row in board_object:
#     if move_data["piece"] in row:
#         piece_exists = True
#         break

# if not piece_exists:
#     return jsonify({"error": "Piece not found on the board."}), 400

# # Call getBmoves, getKBMoves
# if move_data["piece"] == "W":
#     wm = Wmoves(board_object, {"x": 0, "y": 0})
#     wm_all_moves = wm.moves()
# elif move_data["piece"] == "KW":
#     kw = KingWMoves(board_object, {"x": 0, "y": 0})
#     kw_all_moves = kw.moves()
# else:
#     return jsonify({"error": "Invalid piece type."}), 400

# # Check if moves exist
# if not wm_all_moves and not kw_all_moves:
#     return jsonify({"error": "No valid moves available for the piece."}), 400

# # Make the move
# if move_data["piece"] == "W":
#     # Implement logic to make the move for piece "W"
#     pass
# elif move_data["piece"] == "KW":
#     # Implement logic to make the move for piece "KW"
#     pass

# # Update the board
# update_board = UpdateBoard(board_object)
# updated_board = update_board.move_only(move_data)
# game.board = '\n'.join([''.join(row) for row in updated_board])
# db.session.commit()

# # Check for game outcome and update accordingly
# gameLogic = GameLogic(updated_board)
# if gameLogic.check_black_win():
#     gameLogic.update_game_win()
#     game.date_finished = datetime.utcnow()
#     game.winner_id = user_id
#     game.is_draw = False
#     db.session.commit()
#     return jsonify({"message": "You won! Game finished successfully."}), 200
# else:
#     # Implement logic for computer move
#     computer_move, updated_board = PCMove(updated_board)

#     # Update the board with computer move
#     update_board = UpdateBoard(updated_board)
#     updated_board = update_board.move_only(computer_move)
#     game.board = '\n'.join([''.join(row) for row in updated_board])
#     db.session.commit()

#     # Check for game outcome and update accordingly
#     gameLogic = GameLogic(updated_board)
#     if gameLogic.check_white_win():
#         gameLogic.update_game_win()
#         game.date_finished = datetime.utcnow()
#         game.winner_id = get_opponent_id(user_id)
#         game.is_draw = False
#         db.session.commit()
#         return jsonify({"message": "Computer won! Game finished successfully."}), 200

# return jsonify({"message": "Move made successfully.", "board": game.board}), 200

if __name__ == '__main__':
    app.run(port=5555,debug=True)
