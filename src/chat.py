from flask import Blueprint, session, current_app
from flask_socketio import emit, join_room
from src import socketio, session_manager, SessionManager
from src.models import UserModel, UserState, SessionState, SessionModel, db_session, session_votes
from src.utils import send_message_with_delay, send_message, send_server_message_with_delay
import nh3

bp = Blueprint('chat', __name__, url_prefix="/chat")



def is_registered(func):
	def wrapper(*args, **kwargs):
		if 'user' not in session:
			send_message(sockio=socketio, sender_name="Server", room=None, session_id=None, message='User is not registered')
			return
		return func(*args, **kwargs)
	return wrapper

@socketio.on('connect', namespace='/chat')
@is_registered
def handle_connect():
	user_id = session['user']
	with db_session() as db:
		tmp_user = db.query(UserModel).filter_by(id=user_id).one_or_none()
		if current_app.config['DEBUG']:
			send_message(sockio=socketio, sender_name="Server", room=None, session_id=None, message=f'{tmp_user} has connected to /chat')


@socketio.on('disconnect', namespace='/chat')
@is_registered
def handle_disconnect(input):
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
					tmp_user.state = UserState.DISCONNECTED
					disconnect_msg = send_message(sockio=socketio, sender_name="Server", session_id=None, room=current_session.room, message=f'{tmp_user.username} has disconnected!')
					current_session.messages.append(disconnect_msg)
			print(f"User {tmp_user.username} has disconnected!")



##vote_req['round'] should start at 1
@socketio.on('submit_vote', namespace='/chat')
@is_registered
def handle_vote(vote_req):
	if 'round' not in vote_req:
		return
	user_id = session['user']
	round = vote_req['round']
	voted_id = vote_req['voted_id']
	with db_session() as db:
		user = db.query(UserModel).filter_by(id=user_id).one_or_none()
		if user and user.session_id:
			tmp_session = db.query(SessionModel).filter_by(id=user.session_id).one_or_none()
			if tmp_session:
				tmp_room, tmp_id = tmp_session.room, tmp_session.id

				session_manager.handle_vote(user_id=user_id, session_id=tmp_id, round=round, voted_id=voted_id)
				send_server_message_with_delay(sockio=socketio, session_id=tmp_id, room=tmp_room, message="Vote submitted!")





@socketio.on('join', namespace='/chat')
@is_registered
def handle_join(join_req):
	
	if "room" not in join_req or "username" not in join_req:
		send_message(sockio=socketio, sender_name="Server", room=None, session_id=None, message='Error missing room or user field')
		return

	room = join_req["room"]
	username = join_req['username']

	if not room or not username:
		send_message(sockio=socketio, sender_name="Server", room=None, session_id=None, message='username and room fields cannot be empty')
		return
	
	with db_session() as db:
		user_id = session['user']
		tmp_user = db.query(UserModel).filter_by(id=user_id).one_or_none()
		if tmp_user and tmp_user.session_id:
			tmp_session = db.query(SessionModel).filter_by(id=tmp_user.session_id).one_or_none()
			if not tmp_session:
				send_server_message_with_delay(sockio=socketio, session_id=None, room=None, message="Please join a valid session", delay=0)
				return


			#Tie the id to the session object, Set the cookie to the id
			join_room(room)
			print(f'Join: {username} has entered {room}!')
			#Add message to database

			user_num = len(tmp_session.players)
			tmp_msg = send_message(sockio=socketio, sender_name="Server", session_id=None, room=room, message=f'user {user_num}/{SessionManager.MAX_HUMAN_PLAYERS + 1} joined!')

			tmp_session.messages.append(tmp_msg)

			

# On new message
@socketio.on('message', namespace='/chat')
@is_registered
def handle_msg(data):
	if "from" in data:	
		sender = data["from"]
		with db_session() as db:
			tmp_user = db.query(UserModel).filter_by(id=session['user']).one_or_none()
			if tmp_user and tmp_user.state == UserState.ACTIVE:
				if sender == tmp_user.username and "room" in data:
					room = data["room"]
					s = db.query(SessionModel).filter_by(id=tmp_user.session_id).one_or_none()
					if s and s.state != SessionState.INACTIVE and room == s.room: # not a valid session, or session inactive
						if tmp_user in s.players:

							origin = data["message"]
							cleaned_message = nh3.clean(origin)
							if not cleaned_message:
								msg = send_server_message_with_delay(sockio=socketio, session_id=s.id, room=room, message=f"{tmp_user.username} is attempting XSS! Everyone shame them")
								s.messages.append(msg)
								return

							msg = send_message(sockio=socketio, sender_name=sender, session_id=s.id, room=room, message=cleaned_message, include_self=True)
							s.messages.append(msg)
							print([msg.to_dict() for msg in s.messages])
