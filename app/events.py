from app import socketio
from app.utils import detect_scam

@socketio.on('new_message')
def handle_new_message(data):
    result = detect_scam(data['message'])
    socketio.emit('message_result', {
        'message': data['message'],
        'result': "Spam" if result else "Not Spam"
    })
