from quart import websocket
from .models import UserPoints, UserProfile

connected_users = {}

@socket.route('/ws')
async def ws():
    username = await websocket.receive()
    connected_users[username] = websocket

    try:
        while True:
            message = await websocket.receive()
            await handle_message(message)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        del connected_users[username]

async def handle_message(message):
    # Parse and handle incoming messages
    if message.startswith('profile_update:'):
        await update_profile(message)
    elif message.startswith('notification:'):
        await send_notification(message)

async def update_profile(message):
    # Logic to update user profiles
    # Implement profile update based on received data

async def send_notification(user_id, message):
    user_socket = connected_users.get(user_id)
    if user_socket:
        await user_socket.send(message)
