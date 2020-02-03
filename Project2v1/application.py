import os
import requests
import json

import functools
from time import localtime, strftime
from flask_login import LoginManager, current_user, login_required, user_logged_out, user_logged_in
from flask import Flask, render_template, session, url_for, request, flash, redirect
from flask_session import Session
from flask_socketio import SocketIO, emit, send, disconnect, namespace, join_room, leave_room


from models import *


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

# user dictionary to control the session
users = {}
ROOMS = ["lounge", "news", "games", "coding"]

@login.user_loader
def load_user(user_name):
    """ Flask-Login"""
    data_user = {
        users[user_name]: session['user_name']
    }
    return data_user


@app.route("/")
def index():

    return render_template("dashboard.html", rooms=ROOMS, room=session["user_room"])

''' 
@app.route("/logado")
def index():

    return render_template("index.html", user=session["user_name"], users=users, room=session['user_room'])
'''

@app.route('/chat-room',  methods=['POST', 'GET'])
def chat():

    room = request.form.get('room_name')
    print(room)
    name = session['user_name']
    print(name)

    json = {
        "user_name": name,
        "room": room
    }

    return render_template("index.html", json=json, user=name, users=users, room=room)

@app.route('/chat-room')
def leaveTheRoom(json):

    on_leave(json)

def messageReceived(methods=['GET', 'POST']):
    print('message was received')



@socketio.on('new-user')
def new_user(name):
    ''' send back to script.js on the user-connected func '''
    emit('user-connected', name, broadcast=True)


@socketio.on('send-chat-message')
def send_chat_message(json, methods=['GET', 'POST']):
    #socketio.emit('chat-message', json, callback=messageReceived)

    json = {'message': json['message'],
            'user_name': json['user_name'],
            'timestamp': strftime('%b-%d %I:%M%p', localtime()),
            'room': session['user_room']}

    print('received message by send-chat-message ' + str(json))
    socketio.emit('chat-message', json, callback=messageReceived)


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
    sid = request.sid
    users[name] = room

    login_user = User(name, room, sid)

    if not name in session:
        # return render_template("error.html", message="this user is already in session")
        session['user_name'] = name
        session['user_room'] = room
        session['user_sid'] = sid

        json = {"user_name": json['user_name'],
                "room": json['room'],
                "sid": request.sid
                }
        print(str(json))
    else:
        return url_for("chat")

    validate_user_section()
    on_join(json)
    socketio.emit('get-user-info', json, room=room)



@socketio.on('join')
def on_join(data):
    print(data['room'])
    join_room(data['room'])
    socketio.emit('chat-message', {'message': data['user_name'] + " has joined the " + data['room'] + " room "})

@socketio.on('leave')
def on_leave(data):
    ''' Users leave the room '''
    username = str(data['user_name'])
    room = str(data["room"])

    print(username + " is leaving the " + room + " room ")
    socketio.emit('chat-message', {'message': username + " has left the " + room + " room"})

socketio.on('redirect-dashboard')
def on_redirect_dash():

    return redirect(url_for("chat"))

def validate_user_section():
    ''' Validates if a user is into the session, if not rises up an error '''

    if session['user_name'] == None:
        return render_template("error.html", message="User Not in session, please update the page and try again")
    else:
        return redirect(url_for("index"))

@socketio.on('disconnect')
def disconnect():
    socketio.emit('disconnect', session['user_sid'], usercallback=messageReceived)


@app.route('/logout')
def logout():
    # user_logged_out()

    session['user_name'] = None
    session['user_room'] = None
    session['user_sid'] = None

    print("user logged out")
    disconnect()
    return url_for("chat")

if __name__ == '__main__':
    socketio.run(app, debug=True)