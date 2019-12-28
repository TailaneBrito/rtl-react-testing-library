import os

import functools
from flask_login import UserMixin, LoginManager, current_user
from flask import Flask, render_template
from flask_session import Session
from flask_socketio import SocketIO, emit, send, disconnect



app = Flask(__name__)
#app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config['SESSION_TYPE'] = 'filesystem'
#socketio = SocketIO(app)
socketio = SocketIO(app, manage_session=False)

@app.route("/")
def index():
    return render_template("index.html")


def messageReceived(methods=['GET', 'POST']):
    user_name = request.form.get("username")
    print('message was received')

def authenticated_only(f):
    validate_user()

    #if not current_user.is_authenticated:
    if not user_name:
        disconnect()
    else:
        return validate_user()


@socketio.on('my event')
def handle_messages_custom_event(json, methods=['GET', 'POST']):
    print('received message by ' + str(json))
    validate_user()
    socketio.emit('my response', json, callback=messageReceived)


def validate_user():
    user_name = request.form.get("user_name_su")
    
    #if current_user.name is None:
    if user_name is None:
        session['user_name'] = user_name
        current_user.name = user_name


if __name__ == '__main__':
    socketio.run(app, debug=True)