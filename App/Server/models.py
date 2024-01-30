from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()



class Player(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    total_wins = db.Column(db.Integer, default=0)
    total_losses = db.Column(db.Integer, default=0)

    def set_password(self, password):
        self.password_hash = generate_password_hash(str(password))


    def check_password(self, password):
        return check_password_hash(self.password_hash, str(password))
    
    def get_id(self):
        return str(self.id)


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)
    date_started = db.Column(db.DateTime, nullable=True)
    winner_id = db.Column(db.Integer, db.ForeignKey('player.id'))
    moves = db.relationship('Move', backref='game', lazy=True)
    pieces = db.relationship('Piece', backref='game', lazy=True)
    
    def is_active(self):
        return True
    
    def get_existing_game(user_id):
        return Game.query.filter_by(user_id=user_id).first()

class Move(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=False)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)
    move_number = db.Column(db.Integer, nullable=False)
    start_position = db.Column(db.String(2), nullable=False)
    end_position = db.Column(db.String(2), nullable=False)
    is_capture = db.Column(db.Boolean, default=False)
    pieces = db.relationship('Piece', backref='move', lazy=True)

class Piece(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=False)
    position_x = db.Column(db.Integer, nullable=False)
    position_y = db.Column(db.Integer, nullable=False)
    is_king = db.Column(db.Boolean, default=False)
    move_id = db.Column(db.Integer, db.ForeignKey('move.id'))