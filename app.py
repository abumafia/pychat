from flask import Flask, render_template, send_from_directory
from flask_socketio import SocketIO, emit
import json
import os
from datetime import datetime

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="eventlet")

MESSAGES_FILE = 'messages.json'

# Xabarlar faylini o‘qish
def load_messages():
    if os.path.exists(MESSAGES_FILE):
        with open(MESSAGES_FILE, 'r') as f:
            return json.load(f)
    return []

# Xabarlarni saqlash
def save_messages(messages):
    with open(MESSAGES_FILE, 'w') as f:
        json.dump(messages, f)

@app.route('/')
def index():
    return render_template('index.html')

# Statik fayllar (CSS, JS)
@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

@socketio.on('connect')
def handle_connect():
    messages = load_messages()
    emit('load messages', messages)

@socketio.on('chat message')
def handle_message(data):
    data['time'] = datetime.now().strftime('%H:%M:%S')
    messages = load_messages()
    messages.append(data)
    save_messages(messages)
    emit('chat message', data, broadcast=True)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    socketio.run(app, host='0.0.0.0', port=port)