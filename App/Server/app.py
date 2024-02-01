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
    [" ", "B", " ", "W", " ", "W", " ", "W"],
    ["W", " ", "W", " ", "W", " ", "W", " "],
    [" ", "W", " ", "W", " ", "W", " ", "W"],
    [" ", " ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", "B", " ", " ", " ", " "],
    ["B", " ", "", " ", "B", " ", "B", " "],
    [" ", "B", " ", "B", " ", "B", " ", "B"],
    ["B", " ", "B", " ", "W", " ", "B", " "],
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

    # Query the database to find the user by username
    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Check if the provided password matches the stored password
    if user.password != password:
        return jsonify({'error': 'Invalid password'}), 401

    # If both username and password are valid, return user details
    user_details = {
        'id': user.id,
        'username': user.username,
        # Add other user details as needed
    }

    return jsonify(user_details), 200

@app.route("/board/<int:id>", methods=['GET'])
def get_board(id):
    user = User.query.filter_by(id=id).first()
    board = json.loads(user.game.board)
    return jsonify(board)

@app.route("/valid-moves", methods=['POST'])
def valid_moves():
    data = request.get_json()
    user_id = data["id"]
    board = get_user_board(user_id)
    print(board)

    co = data['FROM']

    piece = board[co['y']][co['x']]
    print(f"piece is, {piece}")

    updated = UpdateBoard(board=board)
    if piece == 'B':
        b = Bmoves(board, co)
        bmoves = b.moves()
        new_board = updated.valid_moves(bmoves)
        return jsonify({"board": new_board, "valid_moves": bmoves})

    if piece == 'KB':
        kb = KingBMoves(board, co)
        kbmoves = kb.moves()
        new_board = updated.valid_moves(kbmoves)
        return jsonify({"board": new_board, "valid_moves": kbmoves})

    return {"error": True, "message": "invalid piece"}


from flask import request, jsonify
import json

@app.route("/board/move", methods=["PUT"])
def move():
    data = request.get_json()
    game_id = data['id']
    fr = data['from']
    to = data['to']

    # Assuming get_user_board returns a dictionary with 'board' and 'id'
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
        # Convert nb to JSON-serializable format (list or any other appropriate format)
        nb_serializable = list(nb)
        Game.query.filter_by(id=game_id).update({'board': json.dumps(nb_serializable)})
        db.session.commit()

    print(move_result)
    return jsonify(move_result)

if __name__ == '__main__':
    app.run(port=5555, debug=True)