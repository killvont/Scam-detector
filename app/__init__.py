from flask import Flask
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate  # Import Flask-Migrate

db = SQLAlchemy()
socketio = SocketIO()
migrate = Migrate()  # Initialize Flask-Migrate

def create_app():
    app = Flask(__name__)

    # Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/rhona/OneDrive/Desktop/Scam_Detector/data/scam_detector.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['CORS_HEADERS'] = 'Content-Type'

    # Initialize extensions
    db.init_app(app)
    socketio.init_app(app)
    CORS(app)  # Enable CORS for all routes
    migrate.init_app(app, db)  # Initialize Flask-Migrate with app and db

    with app.app_context():
        from app.routes import main  # Import routes here to avoid circular imports
        app.register_blueprint(main)  # Register the Blueprint
        db.create_all()  # Create database tables (if needed)

    return app
