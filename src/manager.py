import random, enum
from src.utils import send_message_with_delay, send_server_message_with_delay
from src.models import SessionModel, SessionState, UserModel, UserState, MessageModel, db_session
from flask_socketio import SocketIO
from sqlalchemy.exc import SQLAlchemyError, NoResultFound

from datetime import datetime


MAX_HUMAN_PLAYERS = 4 


class SessionManager():

    def __init__(self, users = {}, pending_sessions=[], active_sessions=[]):
        self.users = users
        self.pending_sessions = pending_sessions
        self.active_sessions = active_sessions

    def handle_session(self, socketio : SocketIO, session_id : int, session_room : str):
        print(f"Handling session {session_id}...")

        #Generate robot user id here
        robot_name = "NotABot"

        #Starting message
        send_message_with_delay(sockio=socketio, sender_name=robot_name, 
                                     session_id=session_id, room=session_room, message="Game is starting!")

        #Prompt message, 
        send_message_with_delay(sockio=socketio, sender_name=robot_name, 
                                     session_id=session_id, room=session_room, message="Some prompt here! Goodluck!")
        
        #Main game loop, Basically while the session is ACTIVE, do stuff.
        current_state = self.get_session_status(session_id=session_id)
        while current_state == SessionState.ACTIVE:
            with db_session() as db:
                current_session = db.query(SessionModel).filter_by(id=session_id).one_or_none()
                if not current_session: 
                    break
                elif not current_session.enough_players():# Not enough players to continue(need min 2 person and AI)
                    current_session.end_game()
                current_state = current_session.state

                #send_message and store in database if needed
                tmp_msg = send_message_with_delay(sockio=socketio, sender_name=robot_name, session_id=session_id, 
                                            room=session_room, message="MicCheck123", delay=3)
                current_session.messages.append(tmp_msg)

        send_message_with_delay(sockio=socketio, sender_name="Server", session_id=session_id, 
                                            room=session_room, message=f"Gamesession {session_id} has ended...")

    def create_session(self, host_id, room="", sock: SocketIO = None):
        with db_session() as db:
            if db.query(SessionModel).filter_by(room=room).one_or_none():
                return False, "room already exists, please select a different room name."

            new_pending_session = SessionModel(room=room)
            db.add(new_pending_session)
            
            # Assign host and set state
            host = db.query(UserModel).filter_by(id=host_id).one()
            host.state = UserState.ACTIVE
            new_pending_session.players.append(host)
            new_pending_session.set_host(host.id)
            host.session_id = new_pending_session.id            

            return new_pending_session.room, f"New game session created, {room}."


    def join_session(self, user_id, room="", random_room=False, sock: SocketIO = None):
        if not user_id:
            return None, "Error, user_id is None."
        
        try:
            with db_session() as db:                
                current_user : User = db.query(UserModel).filter_by(id=user_id).one()
                current_session : SessionModel = None


                if current_user.state == UserState.ACTIVE:
                    return None, f"user '{current_user.username}' is already in a session."

                if random_room:
                    pending_sessions = db.query(SessionModel).filter_by(state=SessionState.PENDING).all()
                    if len(pending_sessions) == 0:
                        return  None, "No sessions available."
                    current_session = random.choice(pending_sessions)

                else:
                    current_session : SessionModel = db.query(SessionModel).filter_by(room=room).one()
                

                if current_session.get_user_count() < current_session.max_players_allowed:
                    if current_user not in current_session.players and current_session.state == SessionState.PENDING:                    
                        if not current_session.host_id:
                            current_session.host_id = current_user.id
                            
                        current_session.players.append(current_user)
                        current_user.session_id = current_session.id
                        current_user.state = UserState.ACTIVE
                    elif current_session.state != SessionState.PENDING:
                        return None, "Cannot join an ACTIVE session."
                    
                    if current_session.get_user_count() == current_session.max_players_allowed:
                        current_session.start_game()
                    
                        # Start background task for session handling (if required)
                        if sock:
                            sock.start_background_task(self.handle_session, sock, current_session.id, current_session.room)

                    db.add(current_session)
                    return current_session.room, f"{current_user.username} has joined {current_session.room}!"
                
                else:
                    return None, f"{room} is full!"


        except NoResultFound:
            return False, f"Error, {room} not found!"
        
    def disconnect_player(self, user_id):
        with db_session() as db:
            curr_user = db.query(UserModel).filter_by(id=user_id).one_or_none()
            if curr_user:
                curr_session : SessionModel = db.query(SessionModel).filter_by(id=curr_user.session_id).one_or_none()
                print("Curr User, discconnect: ", curr_session)

                if curr_session and curr_user in curr_session.players:
                    curr_session.players.remove(curr_user)

                    if curr_session.is_host(curr_user.id):
                        if curr_session.players:
                            new_host : UserModel = random.choice(curr_session.players)
                            curr_session.set_host(new_host.id)
                        else:
                            curr_session.host_id = None

            db.delete(curr_user)

    def get_session_status(self, session_id):
        with db_session() as db:
            session = db.query(SessionModel).filter_by(id=session_id).one_or_none()
            if session:
                return session.state
            return None

    def set_session_status(self, session_id: int, new_status: SessionState):
        with db_session() as db:
            curr_session = db.query(SessionModel).filter_by(id=session_id).one_or_none()
            if curr_session:
                curr_session.state = new_status



