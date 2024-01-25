from flask_sqlalchemy  import SQLAlchemy
from flask import Flask

db = SQLAlchemy()
        
class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    total_games_played = db.Column(db.Integer, default=0)
    total_wins = db.Column(db.Integer, default=0)
    total_losses = db.Column(db.Integer, default=0)
    games = db.relationship('Game', backref='player', lazy=True)
    moves = db.relationship('Move', backref='player', lazy=True)
    pieces = db.relationship('Piece', backref='player', lazy=True)

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_started = db.Column(db.DateTime, nullable=False)
    date_finished = db.Column(db.DateTime)
    winner_id = db.Column(db.Integer, db.ForeignKey('player.id'))
    is_draw = db.Column(db.Boolean, default=False)
    moves = db.relationship('Move', backref='game', lazy=True)
    pieces = db.relationship('Piece', backref='game', lazy=True)

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