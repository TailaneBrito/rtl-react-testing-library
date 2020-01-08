import os

from flask_login import UserMixin, LoginManager, current_user, login_user, logout_user
from flask import Flask, render_template, session, url_for, request, flash
from flask_session import Session
from flask_socketio import SocketIO, emit, send, disconnect, namespace

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
    print('users ' + name)
    user_section(name)
    emit('user-connected', name, broadcast=True)


@socketio.on('res_user_name')
def res_user_name(user_name, methods=['GET', 'POST']):
    print('received message by request-user-name ' + str(user_name))

    socketio.emit('user_name_session', user_name, callback=messageReceived)



@socketio.on('send-chat-message')
def send_chat_message(json, methods=['GET', 'POST']):
    print('received message by send-chat-message ' + str(json))
    socketio.emit('chat-message', json, callback=messageReceived)


@socketio.on('my event')
def handle_messages_custom_event(json, methods=['GET', 'POST']):
    print('received message by ' + str(json))
    socketio.emit('my response', json, callback=messageReceived)


# Session
def user_section(user_name):
    ''' definies the name for the session user'''
    print('creating session for user ' + user_name)
    users.append({user_name: request.sid})
    session['user_name'] = str(user_name)
    #session['user_id'] = users[user_name]
    print(users[1])

socketio.on('username', namespace='/private')
def receive_username(username):
    users.append({username : request.id})


if __name__ == '__main__':
    socketio.run(app, debug=True)