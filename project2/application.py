import os

from flask import Flask, render_template
from flask_socketio import SocketIO, emit, send

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

@app.route("/")
def index():
    return render_template("index.html")


def messageReceived(methods=['GET', 'POST']):
    print('message was received')


@socketio.on('my event')
def handle_messages_custom_event(json, methods=['GET', 'POST']):
    print('received:' + str(json))
    socketio.emit('my response', json, callback=messageReceived)


@socketio.on('send-chat-message')
def handle_messages(json, methods=['GET', 'POST']):
    message = data
    print('received:' + str(json))
    emit('send-chat-message', json, callback=messageReceived)


if __name__ == '__main__':
    socketio.run(app, debug=True)