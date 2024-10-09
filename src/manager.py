import random, time, json
from src.utils import send_message_with_delay, send_server_message_with_delay, emit_message
from src.models import SessionModel, SessionState, UserModel, UserState, MessageModel, db_session, delete_by_id, session_votes
from flask_socketio import SocketIO
from sqlalchemy.exc import  NoResultFound
from src.robot import RobotController, RobotType


MAX_HUMAN_PLAYERS = 1
MAX_TIME = 15 # In seconds, right now 15 for testing


class SessionManager():

    def __init__(self, users = {}, pending_sessions=[], active_sessions=[]):
        self.users = users
        self.pending_sessions = pending_sessions
        self.active_sessions = active_sessions

        ## Initiate clean up background task



    def handle_session(self, socketio : SocketIO, session_id : int, session_room : str):
        print(f"Handling session {session_id}...")
        #Generate robot user id here
        with db_session() as db:
            robot_name = RobotController.simple_ask(ask="Generate a simple cool username like 'notabot' or 'smoot'")
            robot_user = UserModel(username=robot_name, state=UserState.ACTIVE)
            robot_user.session_id = session_id

            tmp_session = db.query(SessionModel).filter_by(id=session_id).one_or_none()
            if tmp_session:
                tmp_session.players.append(robot_user)
            else:
                return
            
            db.add(robot_user)
            db.flush()
            

            robot_user_id = robot_user.id
            current_state = tmp_session.state


        #Starting message
        send_server_message_with_delay(sockio=socketio, session_id=session_id, room=session_room, message="Session is starting in 10s...")
        socketio.sleep(10)
        #Main game loop, Basically while the session is ACTIVE, do stuff.
        robot = RobotController(RobotType.gpt3_5, robot_name=robot_name)

        ## Run a round, rounds are indexed starting at 1##
        ##########################################################################################################################################
        emit_message(sockio=socketio, action='session_start', room=session_room, data={"msg" : "Session started."}, delay=0)
        for i in range(1,3):
            send_server_message_with_delay(sockio=socketio, session_id=session_id, room=session_room, message=f"<h1>Round {i} started!</h1><p>There is a bot among you...</p>")
            start_time = time.time()
            emit_message(sockio=socketio, action='round_start', room=session_room, data={"round" : i}, delay=0)

            while current_state == SessionState.ACTIVE:
                # Elapsed time 2 minutes?
                elapsed_time = time.time() - start_time
                if  elapsed_time >= MAX_TIME:
                    break

                with db_session() as db:
                    current_session = db.query(SessionModel).filter_by(id=session_id).one_or_none()
                    current_state = current_session.state

                    # Reasons to end game here
                    if not current_session or not current_session.enough_players():# Not enough players to continue(need min 2 person and AI)
                        break
                
                socketio.sleep(3)

                try:
                    ai_response = robot.get_response(session_id=session_id)
                    if ai_response:
                        ai_response_json = json.loads(ai_response)
                        if "message" in ai_response_json:
                            send_message_with_delay(sockio=socketio, sender_name=ai_response_json['from'].strip("'"), session_id=session_id, room=session_room, message=ai_response_json['message'])
                except Exception as e:
                    print(e)
                    
            emit_message(sockio=socketio, action='round_end', room=session_room, data={"round" : i}, delay=0)
            send_server_message_with_delay(sockio=socketio, session_id=session_id, room=session_room, message=f"<h1>Round {i} finished!</h1><span>chat disabled</span>")
            ##########################################################################################################################################

            # clients will trigger ("submit_vote")
            ## Conduct Voting for said round##
                ## Trigger voting action for socketio
                ## Collect casted votes, if connection issues, player vote not counted
                ## Determine who gets voted out
                ## Determine if players or AI wins

            with db_session() as db:
                tmp_session = db.query(SessionModel).filter_by(id=session_id).one_or_none()
                if(tmp_session):
                    tmp_session.state = SessionState.INACTIVE

            with db_session() as db:
                tmp_session = db.query(SessionModel).filter_by(id=session_id).one_or_none()
                emit_message(sockio=socketio, action="begin_vote", room=session_room, data={'begin_voting' : True, "round" : i, "users" : [p.to_dict() for p in tmp_session.players]})
                socketio.sleep(10)
                emit_message(sockio=socketio, action="stop_vote", room=session_room, data={'stop_voting' : True, "round" : i})
            
            with db_session() as db:
                tmp_session = db.query(SessionModel).filter_by(id=session_id).one_or_none()
                if(tmp_session):
                    tmp_session.state = SessionState.ACTIVE



        ##########################################################################################################################################

        


        ##Cleanup##
        emit_message(sockio=socketio, action='session_end', room=session_room, data={"room" : session_room}, delay=0)
        self.end_session(session_id=session_id, robot_user_id=robot_user_id, socketio=socketio)
        print(f"Session {session_id} has ended...")
        ##########################################################################################################################################


    def create_session(self, host_id, room="", sock : SocketIO = None):
        with db_session() as db:
            if db.query(SessionModel).filter_by(room=room).one_or_none():
                return False, "room already exists, please select a different room name."
            
            current_user : UserModel = db.query(UserModel).filter_by(id=host_id).one_or_none()
            if not current_user:
                return False, f"user with id {host_id}, does not exist"
            else:
                if current_user.state == UserState.ACTIVE and current_user.session_id:
                    return None, f"user '{current_user.username}' is already in a session."
                
            new_pending_session = SessionModel(room=room, max_players_allowed=MAX_HUMAN_PLAYERS)
            db.add(new_pending_session)
            db.commit()
            
            self.add_user(session_id=new_pending_session.id, user_id=host_id, sock=sock)
              

            return new_pending_session.room, f"New game session created, {room}."


    def join_session(self, user_id, room="", random_room=False, sock: SocketIO = None):
        if not user_id:
            return None, "user_id is null"
        
        try:
            with db_session() as db:                
                current_user : UserModel = db.query(UserModel).filter_by(id=user_id).one()
                current_session : SessionModel = None


                if current_user.state == UserState.ACTIVE and current_user.session_id:
                    return None, f"user '{current_user.username}' is already in a session."

                if random_room:
                    pending_sessions = db.query(SessionModel).filter_by(state=SessionState.PENDING).all()
                    if len(pending_sessions) == 0:
                        return  None, "No sessions available."
                    current_session = random.choice(pending_sessions)

                else:
                    current_session : SessionModel = db.query(SessionModel).filter_by(room=room).one()

                self.add_user(session_id=current_session.id, user_id=current_user.id, sock=sock)
                db.add(current_session)
                return current_session.room, f"{current_user.username} has joined {current_session.room}!"
  

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

    def end_session(self, session_id, robot_user_id, socketio):
        with db_session() as db:
            tmp_session = db.query(SessionModel).filter_by(id=session_id).one_or_none()
            if tmp_session:
                tmp_session.state = SessionState.INACTIVE
                send_message_with_delay(sockio=socketio, sender_name="Server", session_id=session_id, 
                                    room=tmp_session.room, message=f"Session has ended...")
                socketio.emit('session_end', {"didEnd" : True})
                
                for p in tmp_session.players:
                    p.state = UserState.WAITING
                    p.session_id = None

                if robot_user_id:
                    socketio.start_background_task(delete_by_id, robot_user_id, UserModel, random.randint(1,4), socketio)
                return True
            return False

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

    def add_user(self, session_id, user_id, sock):
        with db_session() as db:
            user = db.query(UserModel).filter_by(id=user_id).one()
            tmp_session = db.query(SessionModel).filter_by(id=session_id).one()

            room_for_more_players = tmp_session.get_user_count() < tmp_session.max_players_allowed
            player_not_active = user.state != UserState.ACTIVE
            session_pending = tmp_session.state == SessionState.PENDING

            if session_pending and player_not_active and room_for_more_players:
                if not tmp_session.host_id:
                    tmp_session.set_host(user.id)
                
                user.state = UserState.ACTIVE
                tmp_session.players.append(user)
                user.session_id = tmp_session.id

                if tmp_session.get_user_count() >= tmp_session.max_players_allowed:
                    tmp_session.start_game()
                
                    # Start background task for session handling
                    if sock:
                        sock.start_background_task(self.handle_session, sock, tmp_session.id, tmp_session.room)

                return True
            else:
                print("Room for more players:", room_for_more_players)
                print("Player not active:", player_not_active)
                print("Session pending:", session_pending)
                return False
            
    def handle_vote(self, user_id : int, session_id : int, round : int, voted_id : int, ):
        with db_session() as db:
            tmp_session = db.query(SessionModel).filter_by(id=session_id).one_or_none()

            if tmp_session and tmp_session.state == SessionState.INACTIVE:
                #If vote array exits, update current set current round to vote

                vote_entry = db.query(session_votes).filter_by(session_id=session_id, user_id=user_id).one_or_none()
                if vote_entry:
                    # If the user has already voted in this session, update the existing votes_per_round JSON
                    user_voted_per_round = vote_entry.user_voted_per_round
                    # Add or update the vote for the current round
                    user_voted_per_round[round - 1] = voted_id  # Assuming 0-indexed rounds in the list
                    
                    db.execute(session_votes.update()
                        .where(session_votes.c.session_id == session_id)
                        .where(session_votes.c.user_id == user_id)
                        .values(user_voted_per_round=user_voted_per_round))

                else:
                    # If the user hasn't voted in this session yet, create a new entry
                    size = len(tmp_session.players)
                    new_votes_per_round = [None] * (size if size >= 1 else 1)  # Create a list with 'None' for past rounds
                    new_votes_per_round[round - 1] = voted_id
                    
                        # Insert the new vote entry
                    vote_entry = session_votes.insert().values(session_id=session_id, user_id=user_id, user_voted_per_round=new_votes_per_round)
                    db.execute(vote_entry)
                
                print(f"User(id: {user_id}) submitted vote!")
                

