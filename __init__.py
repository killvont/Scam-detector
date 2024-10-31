from flask import Flask
from flask_socketio import SocketIO
from app.config import Config

# Initialize the Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize SocketIO
socketio = SocketIO(app, cors_allowed_origins='*')

# Import routes and models
from app import routes, models

# SocketIO event example
@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

def run():
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)

if __name__ == '__main__':
    run()
