from flask import Blueprint, session
from flask_socketio import emit, join_room
from src import socketio, session_manager
from src.models import UserModel, UserState, MessageModel, SessionModel, db_session
from src.utils import send_message_with_delay, send_message, send_server_message_with_delay
from datetime import datetime

bp = Blueprint('chat', __name__, url_prefix="/chat")



def is_registered(func):
	def wrapper(*args, **kwargs):
		if 'user' not in session:
			send_message(sockio=socketio, sender_name="Server", session_id=None, message='User is not registered')
			return
		return func(*args, **kwargs)
	return wrapper

@socketio.on('connect', namespace='/chat')
@is_registered
def handle_connect():
	user = session['user']
	print("Connect:", {"user_id" : user})


@socketio.on('disconnect', namespace='/chat')
@is_registered
def handle_disconnect():
		user_id = session['user']
		#Everything below can become a session manager function
		with db_session() as db:
			tmp_user = db.query(UserModel).filter_by(id=user_id).one_or_none()
			if tmp_user:
				if tmp_user.session_id: # is there a session?
					current_session = db.query(SessionModel).filter_by(id=tmp_user.session_id).one_or_none() 
					print(current_session)
					if current_session:
						session_manager.disconnect_player(tmp_user.id)
						disconnect_msg = send_message(sockio=socketio, sender_name="Server", session_id=None, room=current_session.room, message=f'{tmp_user.username} has disconnected!')
						current_session.messages.append(disconnect_msg)
				print(f"User {tmp_user.username} has disconnected!")

	
@socketio.on('join', namespace='/chat')
@is_registered
def handle_join(join_req):
	
	room = join_req["room"]
	username = join_req['username']

	if not room or not username:
		emit('error', {'msg': 'Username and room name are required!'})
		return
	
	with db_session() as db:
		user_id = session['user']
		tmp_user = db.query(UserModel).filter_by(id=user_id).one_or_none()
		print(tmp_user)
		if not tmp_user or not tmp_user.session_id:
			send_server_message_with_delay(sockio=socketio, session_id=None, room=None, message="Please join a valid session", delay=0)
			return
		tmp_session = db.query(SessionModel).filter_by(id=tmp_user.session_id).one_or_none()

		print(tmp_session)

		#Tie the id to the session object, Set the cookie to the id
		join_room(room)
		print(f'Join: {username} has entered {room}!')
		tmp_msg = send_message(sockio=socketio, sender_name="Server", session_id=None, room=room, message=f'{tmp_user.username} has entered the chat!')
		
		#Add message to database
		tmp_session.messages.append(tmp_msg)

# On new message
@socketio.on('message', namespace='/chat')
@is_registered
def handle_msg(data):
	if "from" in data:	
		sender = data["from"]
		with db_session() as db:
			tmp_user = db.query(UserModel).filter_by(id=session['user']).one_or_none()
			if not tmp_user:
				return
			elif sender == tmp_user.username and "room" in data:
				room = data["room"]
				s = db.query(SessionModel).filter_by(id=tmp_user.session_id).one_or_none()
				if not s: # not a valid session, cant send messages
					return
				if tmp_user in s.players:
					message = data["message"]


					msg = send_message(sockio=socketio, sender_name=sender, session_id=s.id, room=room, message=message, include_self=False)
					s.messages.append(msg)
					print([msg.to_dict() for msg in s.messages])
