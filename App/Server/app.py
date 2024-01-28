from flask import Flask, redirect, url_for, request, jsonify
from flask_cors import CORS
from models import db, Player  
import json
# from flask_login import LoginManager,login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  
app.config['SECRET_KEY'] = 'your_secret_key'
CORS(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)




# login_manager = LoginManager(app)
# login_manager.login_view = 'login'


with app.app_context():
    db.create_all()

# @login_manager.player_loader
def load_user(user_id):
    return Player.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = Player.query.filter_by(username=username).first()
        if Player and check_password_hash(user.password, password):
            login_user(Player)
            return redirect(url_for('dashboard'))
        else:
            flash('Login failed. Check your username and password.')
    return render_template('login.html')

#the below may or may not change depending on the front-end  
@app.route('/dashboard')
# @login_required
def dashboard():
    return f'Hello, {current_user.username}! You are now logged in.'

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

@app.route('/logout')
# @login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=5555,debug=True)
