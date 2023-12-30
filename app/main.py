from flask import Flask, render_template,request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

# Store user information (socket_id: user_id)
users = {}

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    user_id = generate_user_id()
    users[request.sid] = user_id
    emit('update_messages', f'User {user_id} has joined the chat.', broadcast=True)

@socketio.on('message')
def handle_message(data):
    user_id = users[request.sid]
    emit('update_messages', f'User {user_id}: {data}', broadcast=True)

@socketio.on('disconnect')
def handle_disconnect():
    user_id = users.pop(request.sid)
    emit('update_messages', f'User {user_id} has left the chat.', broadcast=True)

def generate_user_id():
    import uuid
    return str(uuid.uuid4())[:8]

if __name__ == '__main__':
    socketio.run(app)
