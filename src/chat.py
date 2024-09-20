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
		print("User connected:", {"username" : user})
		
	
@socketio.on('disconnect', namespace='/chat')
def handle_disconnect():
	if 'user' in session:
		username = session['user']
		print(username, "has disconnected.")
		emit('message', {'from' : "Server" ,'message' : f'{username} has disconnected!'})


	
@socketio.on('join', namespace='/chat')
def handle_join(join_req):
	''' '''
	if 'user' in session:
		print(join_req)
		room = join_req["room"]
		username = join_req['username']

		if not room or not username:
			emit('error', {'msg': 'Username and room name are required!'})
			return

		#Tie the id to the session object, Set the cookie to the id
		join_room(room)
		print(f'{username} has entered {room}!')
		emit('message', {'from' : "Server" ,'message' : f'{username} has entered {room}!'}, room=room)

# Process room here
@socketio.on('message', namespace='/chat')
def handle_msg(data):	
	if 'user' in session:	
		message = data["message"]
		sender = data["from"]
		room = data["room"]
		print(data)
		#username = data["user"]["name"]
		#send({"text": data['text'] ,"user":{"name": username,"icon": username[0]},"timestamp": data["timestamp"]}, to="lobby")
		emit("message", {"message" : message, "from" : sender}, room=room)


@bp.route("/")
def chat():
		return render_template("chat.html")


def bg_task():
	while True:
		socketio.sleep(3)
		socketio.emit('message', {'msg': 'Background task update'}, namespace='/chat')
