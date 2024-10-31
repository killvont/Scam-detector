import os
import logging
from flask import Flask
from flask_socketio import SocketIO
from app import create_app  # Import your app factory

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load the application configuration
app = create_app()

# Initialize SocketIO
socketio = SocketIO(app, cors_allowed_origins="*")  # Allow all origins for CORS

# Define a function to handle exceptions globally
@app.errorhandler(Exception)
def handle_exception(e):
    """Handle exceptions globally."""
    logger.error(f"An error occurred: {str(e)}")
    response = {
        "error": "Internal Server Error",
        "message": str(e)  # Include the error message for debugging (remove or mask in production)
    }
    return response, 500

# Define a custom command for running the application
@app.cli.command('run')
def run():
    """Run the Flask application."""
    try:
        logger.info("Starting the Flask application...")
        # Use eventlet or threading based on installed packages
        socketio.run(app, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)
    except Exception as e:
        logger.error(f"Failed to start the application: {str(e)}")
        exit(1)  # Exit with error code if the server fails to start

if __name__ == '__main__':
    run()
