# app/routes.py
from flask import jsonify, request
from app import app
from app.socket import socketio  # Import socketio from the new module
from app.utils import detect_scam, process_new_messages, fetch_facebook_listing

@app.route('/detect', methods=['POST'])
def detect():
    messages = request.json.get('messages', [])
    results = process_new_messages(messages)
    return jsonify(results)

@socketio.on('new_message')
def handle_new_message(data):
    result = detect_scam(data['message'])
    socketio.emit('message_result', {'message': data['message'], 'result': "Spam" if result else "Not Spam"})

@app.route('/scan_listing', methods=['POST'])
async def scan_listing():
    data = request.json
    link = data.get('link')
    access_token = data.get('access_token')

    if not link or not access_token:
        return jsonify({'error': 'Link and access token are required.'}), 400

    result = await fetch_facebook_listing(link, access_token)

    if 'error' in result:
        return jsonify({'error': result['error']}), 400

    return jsonify(result)
