from flask import Flask, jsonify, request
import json
from models import db, User, Game
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from All_pieces import Bmoves, KingBMoves
from Moves import Moves
from Checkers import makemove
from UpdateBoard import UpdateBoard

app = Flask(__name__, template_folder='/Users/bonganimasemola/Development/coding/PHASE4/bonganimasemola-Phase4-Checkers-ServerSide/App/Server/templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'

db.init_app(app)
migrate = Migrate(app, db)

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

@app.route('/')
def home():
    data = {'Server side': 'Checkers'}
    return jsonify(data), 200



@app.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()
    username = data['username']
    password = data['password']

    user = User.query.filter_by(username=username).first()

    if user:
        return jsonify({'error': True, 'message': 'user already exists'}), 400

    json_board = json.dumps(original_board)
    game = Game(board=json_board)
    db.session.add(game)
    db.session.commit()
    new_user = User(username=username, password=password, game_id=game.id)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'id': new_user.id, 'game_id': game.id})

def get_user_board(id):
    user = User.query.filter_by(id=id).first()
    board = json.loads(user.game.board)
    return {'board': board, 'id': user.game.id}

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Missing username or password'}), 400

   
    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({'error': 'User not found'}), 404

    
    if user.password != password:
        return jsonify({'error': 'Invalid password'}), 401

    
    user_details = {
        'id': user.id,
        'username': user.username,
        
    }

    return jsonify(user_details), 200

@app.route("/board/<int:id>", methods=['GET'])
def get_board(id):
    user = User.query.filter_by(id=id).first()
    board = json.loads(user.game.board)
    return jsonify(board)


@app.route("/valid-moves", methods=['POST'])
def valid_moves():
    try:
        data = request.get_json()
        user_id = data.get("id")
        if user_id is None:
            return jsonify({"error": True, "message": "User ID not provided"}), 400

        board_data = get_user_board(user_id)
        board = board_data.get('board')
        if board is None:
            return jsonify({"error": True, "message": "Invalid user ID"}), 404

        print("Received board:", board)

        from_coordinates = data.get('FROM')
        if from_coordinates is None or 'x' not in from_coordinates or 'y' not in from_coordinates:
            return jsonify({"error": True, "message": "Invalid FROM coordinates"}), 400

        x, y = from_coordinates['x'], from_coordinates['y']
        piece = board[y][x]
        print(f"Piece at ({x}, {y}): {piece}")

        updated_board = UpdateBoard(board=board)

        if piece == 'B':
            b = Bmoves(board, from_coordinates)
            bmoves = b.moves()
            new_board = updated_board.valid_moves(bmoves)
            return jsonify({"board": new_board, "valid_moves": bmoves})

        if piece == 'KB':
            kb = KingBMoves(board, from_coordinates)
            kbmoves = kb.moves()
            new_board = updated_board.valid_moves(kbmoves)
            return jsonify({"board": new_board, "valid_moves": kbmoves})

        return jsonify({"error": True, "message": "Invalid piece"}), 400

    except Exception as e:
        print(f"Error in valid_moves: {e}")
        return jsonify({"error": True, "message": "Internal server error"}), 500

@app.route("/board/move", methods=["PUT"])
def move():
    data = request.get_json()
    game_id = data['id']
    fr = data['from']
    to = data['to']

   
    user_game = get_user_board(game_id)
    print(f'{user_game}')
    board = user_game['board']
    print(f'{board}')
    game_id = user_game['id']
    print(f'{game_id}')

    move_result = makemove(fr, to, board)
    print(move_result)

    if 'board' in move_result:
        nb = move_result['board']
        nb_serializable = list(nb)
        Game.query.filter_by(id=game_id).update({'board': json.dumps(nb_serializable)})
        db.session.commit()

    print(move_result)
    return jsonify(move_result)

if __name__ == '__main__':
    app.run(port=5555, debug=True)