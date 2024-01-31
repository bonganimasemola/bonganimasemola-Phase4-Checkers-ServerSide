from flask import Flask, jsonify, json, request
from models import db,User, Game
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from All_pieces import Bmoves, KingBMoves
from Moves import Moves
from UpdateBoard import UpdateBoard
app = Flask(__name__, template_folder='/Users/bonganimasemola/Development/coding/PHASE4/bonganimasemola-Phase4-Checkers-ServerSide/App/Server/templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  
app.config['SECRET_KEY'] = 'your_secret_key'

db.init_app(app)
# db = SQLAlchemy(app)
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

    user = User.query.filter_by(username = username).first()

    if user:
        return jsonify({'error':True, 'message': 'user already exists' }), 400
    
    json_board = json.dumps(original_board)
    game= Game(board=json_board)
    db.session.add(game)
    db.session.commit()
    new_user = User(username=username, password=password, game_id=game.id)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'id': new_user.id, 'game_id': game.id})

def get_user_board(id):
    user = User.query.filter_by(id=id).first()
    board = json.loads(user.game.board)
    return board
@app.route("/board/<int:id>", methods=['GET'])
def get_board(id):
    user = User.query.filter_by(id=id).first()
    board=json.loads(user.game.board)
    return jsonify(board)

@app.route("/board/valid-moves", methods=['POST'])
def valid_moves():
    data = request.get_json()
    user_id = data["id"]
    board= get_user_board(user_id)
    print(board)

    co=data['FROM']

    piece = board[co['y']][co['x']]  
    print(f"piece is, {piece}")

    updated = UpdateBoard(board=board)
    if piece == 'B':
        b = Bmoves(board, co)
        bmoves= b.moves()
        new_board = updated.valid_moves(bmoves)
        return jsonify({"board": new_board, "valid_moves":bmoves})
    
    if piece == 'KB':
        kb = KingBMoves(board, co)
        kbmoves = kb.moves()
        new_board = updated.valid_moves(kbmoves)
        return jsonify({"board": new_board, "valid_moves":kbmoves})
    
    return {"error": True, "message": "invalid piece"}

@app.route("/board/move", methods=['PUT'])
def make_a_move():
      data = request.get_json()
      id = data['id']
      to=data['to']
      fr=data['from']

      game=get_user_board(id)
      board =game['board']
      game_id=game['id']
    
      move = move(fr, to, board)

if __name__ == '__main__':
    app.run(port = 5555, debug=True)