import os
import json

import functools
from flask_login import LoginManager, current_user, login_required, user_logged_out, user_logged_in
from flask import Flask, render_template, session, url_for, request, flash, redirect
from flask_session import Session
from flask_socketio import SocketIO, emit, send, disconnect, namespace

# user dictionary to control the session
users = {}

app = Flask(__name__)

# Env configuration
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["SESSION_PERMANENT"] = False
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)
socketio = SocketIO(app, manage_session=False)

# Flask-Login : --- Setup ---------------------------------------
login_manager = LoginManager()
login_manager.init_app(app)

sess = Session()
print(sess)


@login_manager.user_loader
def user_loader(user_name):
    """ Flask-Login"""
    data_user = {
        users[user_name] : session['user_name']
    }
    return data_user


@app.route("/")
def log():

    # return render_template("dashboard.html")
    # if user_logged_in is True:
    return render_template("dashboard.html")


@app.route("/logado", methods=["GET", "POST"])
def index():

    return render_template("index.html", user=session["user_name"], users=users)


def messageReceived(methods=['GET', 'POST']):
    print('message was received')


@socketio.on('connect')
def connection_on():
    message = 'new user is connecting...'
    emit('my response ', message)


@socketio.on('new-user')
def new_user(name):
    #user_section(name)
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
    # user_section(json)
    socketio.emit('my response', json, callback=messageReceived)


# Session
@socketio.on('get-user')
def user_section(json, methods=['GET', 'POST']):
    ''' action on dashboard.js connect '''
    ''' definßes the name for the session user '''
    print('creating session for user ' + str(json))
    name = json['user_name']
    print(name)
    users[name] = request.sid
    session['user_name'] = name
    session['user_sid'] = request.sid
    print(users)

    validate_user_section()


@socketio.on('channel')
def get_channel_name(json, methods=['GET', 'POST']):
    print('action on dashboard.htm channel ' + str(json))

    channel = json['channel']
    channel_user = json['user']

    print("{} {}".format(channel, channel_user))


def validate_user_section():
    ''' Validates if a user is into the session, if not rises up an error '''

    if session['user_name'] == None:
        return render_template("error.html", message="Create #1 Invalid user name or password, please type one.")

@app.route('/logout')
def logout():

    if not session['user_name'] == None:
        flash('user {} successfully. see you later!!!'.format(session['user_name']))
        session['user_name'] = None
    else:
        flash('Login in to start')
        return render_template("dashboard.html")


if __name__ == '__main__':
    socketio.run(app, debug=True)