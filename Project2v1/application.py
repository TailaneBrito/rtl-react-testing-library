import os

from flask_login import UserMixin, LoginManager, current_user, login_user, logout_user
from flask import Flask, render_template, session, url_for, request, flash
from flask_session import Session
from flask_socketio import SocketIO, emit, send, disconnect

users = []

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)
socketio = SocketIO(app, manage_session=False)
login = LoginManager(app)

@login.user_loader
def user_loader(id):
    return User(id)


class User(UserMixin):
    def __init__(self, username):
        self.id = username


@app.route("/")
def index():
    return render_template("index.html")


def messageReceived(methods=['GET', 'POST']):
    print('message was received')

@socketio.on('connect')
def connection_on():
    print('new user is connecting ')


@socketio.on('new-user')
def new_user(name):
    emit('user-connected', name, broadcast=True)


@socketio.on('send-chat-message')
def send_chat_message(json):
    print('received message by send-chat-message ' + str(json))
    socketio.emit('chat-message', json, callback=messageReceived)


@socketio.on('my event')
def handle_messages_custom_event(json, methods=['GET', 'POST']):
    print('received message by ' + str(json))
    socketio.emit('my response', json, callback=messageReceived)


if __name__ == '__main__':
    socketio.run(app, debug=True)