from flask_sqlalchemy import SQLAlchemy



class UserTable():
    def __init__(self, id, username, password, email):
        self.id = id
        self.username = username
        self.password = password
        self.email = email



class MovesTable():
    def __init__(self, id, current_player, board_state, active_pieces, valid_moves, winner, end_conditions):
        self.id = id
        self.current_player = current_player
        self.board_state = board_state
        self.active_pieces = active_pieces
        self.valid_moves = valid_moves
        self.winner = winner
        self.end_conditions = end_conditions


class GamesTable():
    def __init__(self, moves, games_id, captured_pieces, quantity_captured_by_player, player):
        self.moves = moves
        self.games_id = games_id
        self.captured_pieces = captured_pieces
        self.quantity_captured_by_player = quantity_captured_by_player
        self.player = player
