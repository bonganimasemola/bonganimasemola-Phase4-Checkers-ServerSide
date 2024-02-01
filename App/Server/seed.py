from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from models import db, Player, Game, Move, Piece
from flask import Flask
from app import app





app = Flask(__name__)


with app.app_context():
    
    db.init_app(app)
    
    
    db.create_all()

def seed_data():
    
    with app.app_context():
        player1 = Player(username='Player1')
        player2 = Player(username='Player2')
        db.session.add_all([player1, player2])
        db.session.commit()

        game = Game(date_started=datetime.utcnow(), winner_id=player1.id)
        db.session.add(game)
        db.session.commit()

        move1 = Move(game_id=game.id, player_id=player1.id, move_number=1, start_position='A2', end_position='A4')
        move2 = Move(game_id=game.id, player_id=player2.id, move_number=1, start_position='B7', end_position='B5')
        piece1 = Piece(game_id=game.id, player_id=player1.id, position_x=1, position_y=4)
        piece2 = Piece(game_id=game.id, player_id=player2.id, position_x=2, position_y=5)
        db.session.add_all([move1, move2, piece1, piece2])
        db.session.commit()

if __name__ == '__main__':
    seed_data()
    print("Seeded database with example data")
