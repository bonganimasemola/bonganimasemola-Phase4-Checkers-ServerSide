from flask import Flask, redirect, url_for, request, jsonify, render_template, flash
from datetime import datetime
from GameStatus import GameLogic
from UpdateBoard import UpdateBoard
from Moves import Moves
from All_pieces import Bmoves, KingBMoves, Wmoves, KingWMoves
from flask_cors import CORS
from models import db, Player, Game
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
    return Player.query.get(int(user_id))



@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Missing username or password'}), 400

    # Query the database to find the user by username
    user = Player.query.filter_by(username=username).first()

    if user and user.check_password(password):
        # Use Flask-Login's login_user function to log in the user
        login_user(user)
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'error': 'Invalid username or password'}), 401



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
#@app.route('/start_game', methods=['POST'])

@app.route("/start_game", methods=["GET"])
@login_required
def get_board():
    if request.method == "GET":
        board = original_board
        return jsonify({"board": board})
# def start_game():
#     print("Received request to start_game")
#     if current_user.is_authenticated:
#         user_id = current_user.id

#         original_board = request.json.get('board', None)

#         if not original_board:
#             # Create a new game and set the player_id
#             game = Game(player_id=user_id, date_started=datetime.utcnow(), winner_id=None)
#             db.session.add(game)
#             db.session.commit()

#             return jsonify({"message": "Game started successfully.", "game_id": game.id}), 200
#         else:
#             # Retrieve the existing game using the user_id
#             existing_game = get_existing_game(user_id)

#             if existing_game:
#                 return jsonify({"message": "Existing game retrieved successfully.", "board": original_board}), 200
#             else:
#                 # If the existing game is not found, you can return an error or handle it accordingly
#                 return jsonify({"error": "Existing game not found."}), 404
#     else:
#         # Handle the case where the user is not authenticated
#         return jsonify({"error": "User not authenticated."}), 401
    
def get_existing_game(user_id):
    # Query the database to find an existing game for the given user_id
    existing_game = Game.query.filter_by(player_id=user_id).first()
    return existing_game

# Add a helper function to retrieve an existing game
# def get_existing_game(user_id):
    # You need to implement the logic to retrieve an existing game based on the user_id
    # For example, you can query the database for an ongoing game for the user
    # return Game.query.filter_by(player_id=user_id, winner_id=None, is_draw=False).first()

@app.route('/forfeit_game/<int:game_id>', methods=['POST'])
@login_required
def forfeit_game(game_id):
    user_id = current_user.id

    game = Game.query.get(game_id)
    
    if game is None:
        return jsonify({"error": "Game not found."}), 404

    if game.player_id != user_id:
        return jsonify({"error": "You are not authorized to forfeit this game."}), 403

    
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

    
    if 'board' not in data:
        return jsonify({'error': 'Missing "board" key in JSON data'}), 400

    initial_board = data['board']

    
    if not isinstance(initial_board, list) or not all(isinstance(row, list) for row in initial_board):
        return jsonify({'error': 'Invalid format for "board" data'}), 400

    
    new_game = Game(board=initial_board)
    
    try:
        db.session.add(new_game)
        db.session.commit()
        return jsonify({'message': 'Game created successfully', 'game_id': new_game.id}), 201
    except Exception as e:
       
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


# @app.route('/register', methods=['POST'])
# def register():
#     data = request.get_json()
#     name = data['name']
#     email = data['email']
#     password = data['password']

   
#     existing_user = User.query.filter_by(email=email).first()
#     if existing_user:
#         return jsonify({'error': 'User already exists'}), 400

    
#     new_user = User(name=name, email=email, password=password)
#     db.session.add(new_user)
#     db.session.commit()

#     return jsonify({'message': 'User created successfully'}), 201



@app.route('/games/<int:game_id>/move', methods=['POST'])
def make_move(game_id):
    data = request.get_json()
    move = data['move']  

    game = Game.query.get(game_id)
    if not game:
        return jsonify({'error': 'Game not found'}), 404

    
    current_board = game.board

    
    updated_board, promotion = validate_and_make_move(current_board, move)

    if updated_board:
        
        game.board = updated_board

       
        if promotion:
            handle_promotion(updated_board, promotion)

        
        db.session.commit()

        return jsonify({'message': 'Move successful', 'updated_board': updated_board})
    else:
        return jsonify({'error': 'Invalid move'}), 400


def validate_and_make_move(current_board, move):
   
    piece = current_board[move["from"]["y"]][move["from"]["x"]]

    
    if piece == "W" :
        moves_instance = Wmoves(current_board, move["from"])
    elif  piece == "KW":
        moves_instance = KingWMoves(current_board, move["from"])
    elif piece == "KB":
        moves_instance = KingBMoves(current_board, move["from"])
    elif piece == "B": 
        moves_instance = Bmoves(current_board, move["from"])
    else:
        return None  

    all_moves = moves_instance.moves()

   
    if move in all_moves:
        updated_board = update_board(current_board, move)
        promotion = check_for_promotion(updated_board, move)
        return updated_board, promotion
    else:
        return None  


def update_board(board, move):
    
    update_board_instance = UpdateBoard(board)
    updated_board = update_board_instance.move_capture(move)  
    return updated_board


def check_for_promotion(board, move):
    co = move["to"]  
    piece = board[co["y"]][co["x"]]

    if piece == "W" and co["y"] == 7:
        return "KW"
    elif piece == "B" and co["y"] == 0:
        return "KB"
    else:
        return None


def handle_promotion(board, promotion, move):
   
    co = move["to"]  

    if promotion == "KW":
        board[co["y"]][co["x"]] = "KW"
    elif promotion == "KB":
        board[co["y"]][co["x"]] = "KB"
        

if __name__ == '__main__':
    app.run(port=5555,debug=True)
