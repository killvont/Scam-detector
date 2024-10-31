import os
import re
import requests
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from flask_socketio import SocketIO, emit

# Initialize the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your_default_secret_key')  # Use environment variable
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data/scam_detector.db')  # Use environment variable
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
socketio = SocketIO(app, cors_allowed_origins='*')

# User model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(150), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        captcha_response = request.form['g-recaptcha-response']
        captcha_secret = os.environ.get('CAPTCHA_SECRET_KEY')  # Store your secret key in environment variables

        # Validate CAPTCHA
        if not validate_captcha(captcha_secret, captcha_response):
            flash('CAPTCHA validation failed. Please try again.', 'danger')
            return redirect(url_for('register'))

        # Check for existing user
        if User.query.filter_by(username=username).first():
            flash('Username already exists. Please choose a different one.', 'danger')
            return redirect(url_for('register'))

        if User.query.filter_by(email=email).first():
            flash('Email already registered. Please use a different one.', 'danger')
            return redirect(url_for('register'))

        # Password strength check
        if not validate_password_strength(password):
            flash('Password must be at least 8 characters long and include at least one uppercase letter, one lowercase letter, and one digit.', 'danger')
            return redirect(url_for('register'))

        # Hash the password and create new user
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, email=email, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

def validate_captcha(secret, response):
    verification = requests.post(
        f'https://www.google.com/recaptcha/api/siteverify?secret={secret}&response={response}'
    )
    return verification.json().get('success')

def validate_password_strength(password):
    return re.match(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d).{8,}$', password)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and bcrypt.check_password_hash(user.password_hash, request.form['password']):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        flash('Login unsuccessful. Please check your username and password.', 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    return render_template('index.html')

# SocketIO events
@socketio.on('connect')
def handle_connect():
    print('Client connected')
    emit('response', {'message': 'You are connected!'})

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

# Create the data directory if it doesn't exist
if not os.path.exists('data'):
    os.makedirs('data')

# Create the database tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
