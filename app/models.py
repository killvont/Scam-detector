# app/models.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

# Initialize Flask and SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/rhona/OneDrive/Desktop/Scam_Detector/data/scam_detector.db'  # Use absolute path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(UserMixin, db.Model):
    """Model for user accounts."""

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='user')
    profile = db.relationship('UserProfile', backref='user', uselist=False)

    def __repr__(self):
        return f'<User {self.username}>'

class UserProfile(db.Model):
    """Model for user profiles."""

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    avatar_url = db.Column(db.String(200), nullable=True)
    bio = db.Column(db.String(500), nullable=True)
    status = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return f'<UserProfile user_id={self.user_id}>'

class Scam(db.Model):
    """Model for reported scams."""

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    reported_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())  # Track when the scam was reported

    def __repr__(self):
        return f'<Scam {self.title}>'

class UserPoints(db.Model):
    """Model for tracking user points and badges."""

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    points = db.Column(db.Integer, default=0)
    badges = db.Column(db.JSON, default={})  # Default to an empty JSON object

    def __repr__(self):
        return f'<UserPoints user_id={self.user_id}, points={self.points}>'

# Ensure the database is created
with app.app_context():
    db.create_all()
