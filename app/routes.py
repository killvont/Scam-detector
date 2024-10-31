import os
from flask import jsonify, request, Blueprint
from flask_socketio import emit
from app import socketio
from app.utils import process_new_messages, detect_scam, fetch_facebook_listing

# Create a Blueprint for the routes
main = Blueprint('main', __name__)

# Load access token from environment variable or hardcode it for testing (not recommended for production)
ACCESS_TOKEN = os.getenv('FACEBOOK_ACCESS_TOKEN', 'EAAYM2BYeX6IBO4VxXotr1nUQEfnMNwXAudyf9mDi1XZABZCdTJv3Rj3YFx1FT6y2FJnSP9adQCj5ZCZATOBV7ulgL3VRC1JFxeCGz5r1vGWpTFHQ473nZAEc15gFaCCSOXyBfmrfCWot2umtZAxu2pQUvtzT3Ld17frUzEtpMgvGdg7IyHa5XHRYycXPpFOdZAudZAhXbZCgaogT8tqeoqG5TQw2X8kZAhJuMw3ZBB4')

@main.route('/')
def index():
    """Welcome message for the API."""
    return jsonify({"message": "Welcome to the Scam Detector API!"}), 200

@main.route('/detect', methods=['POST'])
def detect():
    """
    Endpoint to detect scams based on received messages.
    Expects a JSON body with a list of messages.
    Example JSON input:
    {
        "messages": ["test message"]
    }
    """
    messages = request.json.get('messages', [])
    if not messages:
        return jsonify({'error': 'No messages provided.'}), 400

    try:
        results = process_new_messages(messages)
        return jsonify(results), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@socketio.on('new_message')
def handle_new_message(data):
    """
    Handle incoming socket messages to detect scams in real-time.
    Emits the result back to the client.
    """
    if 'message' not in data:
        emit('message_result', {'error': 'No message provided.'})
        return

    try:
        result = detect_scam(data['message'])
        emit('message_result', {'message': data['message'], 'result': "Spam" if result else "Not Spam"})
    except Exception as e:
        emit('message_result', {'error': str(e)})

@main.route('/scan_listing', methods=['POST'])
def scan_listing():
    """
    Endpoint to scan a Facebook listing for scams.
    Expects a JSON body with a link.
    Example JSON input:
    {
        "link": "https://example.com"
    }
    """
    data = request.json
    link = data.get('link')

    if not link:
        return jsonify({'error': 'Link is required.'}), 400

    try:
        result = fetch_facebook_listing(link, ACCESS_TOKEN)  # Use the access token

        if 'error' in result:
            return jsonify({'error': result['error']}), 400

        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main.route('/test', methods=['POST'])
def test_route():
    """
    A simple test endpoint to verify that the server is running.
    """
    return jsonify({"message": "Test route is working!"}), 200

@main.route('/favicon.ico')
def favicon():
    """Return a no content response for favicon requests."""
    return '', 204
