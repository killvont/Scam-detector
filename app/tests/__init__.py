# app/__init__.py
from flask import Flask

print("Initializing app...")
app = Flask(__name__)
print("App created.")

# Import socket after app creation
from app.socket import socketio  # Now this imports the initialized socketio
print("SocketIO created.")

# Import routes after defining app and socketio
import app.routes
print("Routes imported.")
