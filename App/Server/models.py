from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
class  User(db.Model):
    __tablename__="users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    game_id = db.Column(db.Integer,db.ForeignKey('game_id'),unique=True)
    game = db.relationship('game',back_populates = 'user', uselist=False)


class Game(db.Model):
    __tablename__='game'
    id = db.Column(db.Integer,primary_key=True)
    board = db.Column(db.String(500), nullable = False)
    user = db.relationship('user', back_populates = 'game')

