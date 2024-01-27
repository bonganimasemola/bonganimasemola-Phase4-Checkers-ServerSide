from flask import Flask, jsonify, request
from flask_cors import CORS
from models import db, Player  

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  
db.init_app(app)


with app.app_context():
    db.create_all()

@app.route('/')
def home():
    data = {'Server side': 'Checkers'}
    return jsonify(data), 200

@app.route('/players', methods=['GET'])
def get_players():
    players = Player.query.all()
    player_list = [{'id': player.id, 'username': player.username} for player in players]
    return jsonify(player_list), 200

@app.route('/players', methods=['POST'])
def create_player():
    data = request.get_json()

    
    if 'username' not in data or 'email' not in data:
        return jsonify({'message': 'Username and email are required'}), 400

    existing_username = Player.query.filter_by(username=data['username']).first()
    existing_email = Player.query.filter_by(email=data['email']).first()

    if existing_username:
        return jsonify({'message': 'Username is already taken'}), 400

    if existing_email:
        return jsonify({'message': 'Email is already registered'}), 400

    new_player = Player(username=data['username'], email=data['email'])
    
    try:
        db.session.add(new_player)
        db.session.commit()
        return jsonify({'message': 'Player created successfully'}), 201
    except:
        db.session.rollback()
        return jsonify({'message': 'Error creating player'}), 500

if __name__ == '__main__':
    app.run(port=5555, debug=True)
