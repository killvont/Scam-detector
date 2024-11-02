from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_socketio import SocketIO
from app.config import Config

# Initialize the Flask application
app = Flask(__name__)
app.config.from_object(Config)

# Ensure essential configurations like SECRET_KEY are set
if not app.config.get('SECRET_KEY'):
    raise RuntimeError("SECRET_KEY is not set in the configuration.")

# Initialize extensions
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # Redirect to login view if not authenticated
socketio = SocketIO(app, cors_allowed_origins='*')

# Load application components
from app import routes, models

# SocketIO events for real-time communication
@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

def run():
    if app.config.get('DEBUG'):
        print("Running in debug mode")
    else:
        print("Running in production mode")
    socketio.run(app, host=app.config.get('HOST', '0.0.0.0'), port=app.config.get('PORT', 5000))

if __name__ == '__main__':
    run()
