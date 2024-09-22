from flask import Blueprint, redirect, session, url_for, render_template
from flask_socketio import emit, join_room, leave_room, send
from src.utils import is_registered
from src import socketio, session_manager
from src.message import Message
from src.session import Session


bp = Blueprint('chat', __name__, url_prefix="/chat")


@socketio.on('connect', namespace='/chat')
def handle_connect():
	if 'user' in session:
		user = session['user']
		print("Connect:", {"username" : user})

@socketio.on('disconnect', namespace='/chat')
@is_registered
def handle_disconnect():
		username = session['user']

		#Everything below can become a session manager function
		if username in session_manager.users:
			tmp_user = session_manager.users[username]
			if tmp_user.session: # is there a session?
				tmp_session = tmp_user.session
				tmp_user.disconnect() # Remove user from Session, user.session becomes null
				if tmp_session.is_running() and not tmp_session.enough_players():
					tmp_session.end_game()
					if tmp_session in session_manager.active_sessions:
						session_manager.active_sessions.remove(tmp_session)
					
				# if tmp_session.get_state() == Session.State.:
				# 	if tmp_session in session_manager.active_sessions:
				# 		session_manager.active_sessions.remove(tmp_session)
			
				emit('message', {'from' : "Server" ,'message' : f'{username} has disconnected!'}, room=tmp_session.room)


			session_manager.users.pop(username)
			print(username, "has disconnected.")


	
@socketio.on('join', namespace='/chat')
def handle_join(join_req):
	if 'user' in session:
		room = join_req["room"]
		username = join_req['username']

		if not room or not username:
			emit('error', {'msg': 'Username and room name are required!'})
			return

		#Tie the id to the session object, Set the cookie to the id
		join_room(room)
		print(f'Join: {username} has entered {room}!')
		emit('message', {'from' : "Server" ,'message' : f'{username} has entered the chat!'}, room=room)

# On new message
@socketio.on('message', namespace='/chat')
def handle_msg(data):
	if 'user' in session and "from" in data:	
		sender = data["from"]
		if sender == session['user'] and "room" in data:
			room = data["room"]
			s = session_manager.get_session(room)
			if not s: # not a valid session, cant send messages
				return
			if sender in s.players:
				message = data["message"]

				msg = Message(sender=sender, message=message, room=room)
				s.messages.append(msg)

				print([m.to_dict() for m in s.messages])
				#username = data["user"]["name"]
				#send({"text": data['text'] ,"user":{"name": username,"icon": username[0]},"timestamp": data["timestamp"]}, to="lobby")
				emit("message", msg.to_dict(), room=room, include_self=False)

