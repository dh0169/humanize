from flask import Blueprint, redirect, session, url_for, render_template
from flask_socketio import emit, join_room, leave_room, send
from src.utils import is_registered


from src import socketio, session_manager
from src.session import Session 


bp = Blueprint('chat', __name__, url_prefix="/chat")


@socketio.on('connect', namespace='/chat')
def handle_connect():
	if 'user' in session:
		user = session['user']
		print({"username" : user})
		emit("connect", {"username" : user})
		join_room("lobby")
		
	
# @socketio.on('disconnect', namespace='/chat')
# def handle_disconnect():
# 	if 'user' in session:
# 		name = session.pop('user')
# 		active_users.remove(name)

	
@socketio.on('join', namespace='/chat')
def handle_join(join_req):
	''' '''
	if 'user' in session:	
		room = join_req["room"]
		type_c = join_req['type']

		if not room or not type_c:
			emit('error', {'msg': 'Username and room name are required!'})
			return

		username = session['user']
		session['user'] = username

		#Tie the id to the session object, Set the cookie to the id
		join_room(room)
		emit('message', {'msg' : f'{username} has entered the chat!'}, room=room)


@socketio.on('message', namespace='/chat')
def handle_msg(data):	
	if 'user' in session:	
		print(data)
		username = data["user"]["name"]
		send({"text": data['text'] ,"user":{"name": username,"icon": username[0]},"timestamp": data["timestamp"]}, to="lobby")
	

@bp.route("/")
def chat():
		return render_template("chat.html")


def bg_task():
	while True:
		socketio.sleep(3)
		socketio.emit('message', {'msg': 'Background task update'}, namespace='/chat')
