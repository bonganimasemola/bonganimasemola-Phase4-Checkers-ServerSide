from flask import Flask, jsonify
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    data = {'Server side': 'Checkers'}
    
    print(data)
    print(jsonify(data))
    return (jsonify(data), 200)

if __name__ == '__main__':
    app.run(port=5555, debug=True)