import os
import json

import functools
from time import localtime, strftime
from flask_login import LoginManager, current_user, login_required, user_logged_out, user_logged_in
from flask import Flask, render_template, session, url_for, request, flash, redirect
from flask_session import Session
from flask_socketio import SocketIO, emit, send, disconnect, namespace, join_room, leave_room

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
login = LoginManager(app)
login.init_app(app)

sess = Session()
print(sess)

ROOMS = ["lounge", "news", "games", "coding"]

@login.user_loader
def load_user(user_name):
    """ Flask-Login"""
    data_user = {
        users[user_name] : session['user_name']
    }
    return data_user


@app.route("/")
def log():

    # return render_template("dashboard.html")
    # if user_logged_in is True:
    return render_template("dashboard.html", rooms=ROOMS)


@app.route("/logado", methods=["GET", "POST"])
def index():

    return render_template("index.html", user=session["user_name"], users=users, room=session['user_room'])


def messageReceived(methods=['GET', 'POST']):
    print('message was received')


@socketio.on('connect')
def connection_on():
    message = 'new user is connecting...'
    emit('my response ', message)


@socketio.on('new-user')
def new_user(name):
    emit('user-connected', name, broadcast=True)


@socketio.on('send-chat-message')
def send_chat_message(json, methods=['GET', 'POST']):
    print('received message by send-chat-message ' + str(json))
    #socketio.emit('chat-message', json, callback=messageReceived)

    json = {'message': json['message'],
            'user_name': json['user_name'],
            'timestamp': strftime('%b-%d %I:%M%p', localtime()),
            'room': session['user_room']}

    socketio.emit('chat-message', json, callback=messageReceived())


@socketio.on('my event')
def handle_messages_custom_event(json, methods=['GET', 'POST']):
    print('received message by ' + str(json))
    # adding function for data pm and am

    #socketio.emit('my response', json, callback=messageReceived)
    socketio.emit('my response', json, callback=messageReceived)




# Session
@socketio.on('get-user')
def user_section(json, methods=['GET', 'POST']):
    ''' action on dashboard.js connect '''
    print('get-user application ' + str(json))
    name = json['user_name']
    room = json['room']

    # session user
    users[name] = request.sid
    session['user_name'] = name
    session['user_room'] = room
    session['user_sid'] = request.sid
    print(users)
    print(session['user_room'])

    validate_user_section()



@socketio.on('channel')
def get_channel_name(json, methods=['GET', 'POST']):
    print('action on dashboard.htm channel ' + str(json))

    channel = json['channel']
    channel_user = json['user']

    print("{} {}".format(channel, channel_user))


@socketio.on('join')
def join(data):
    join_room(data['room'])
    send({'message' : data['user_name'] + "has joined the " + data['room'] +
          "room"}, room=data['room'])


@socketio.on('leave')
def leave(data):
    leave_room(data['room'])
    send({'message': data['user_name'] + "has left the " + data['room'] +
          "room"}, room=data['room'])


def validate_user_section():
    ''' Validates if a user is into the session, if not rises up an error '''

    if session['user_name'] == None:
        return render_template("error.html", message="Create #1 Invalid user name or password, please type one.")

@app.route('/logout')
def logout():

    session['user_name'] = None
    return render_template("dashboard.html")

    ''' 
    if not session['user_name'] == None:
        flash('user {} successfully. see you later!!!'.format(session['user_name']))
        session['user_name'] = None
    else:
        flash('Login in to start')
        return render_template("dashboard.html")
    '''

if __name__ == '__main__':
    socketio.run(app, debug=True)