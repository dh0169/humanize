import random, time, json
from src.utils import send_message_with_delay, send_server_message_with_delay, emit_message
from src.models import SessionModel, SessionState, UserModel, UserState, MessageModel, db_session, delete_by_id, session_votes
from flask_socketio import SocketIO
from sqlalchemy.exc import  NoResultFound
from src.robot import RobotController, RobotType


class SessionManager():
    MAX_HUMAN_PLAYERS = 2
    MIN_HUMAN_PLAYERS_NEEDED = 2
    MAX_TIME = 75 # In seconds, right now 15 for testing
    VOTE_TIME = 25

    def __init__(self, users = {}, pending_sessions=[], active_sessions=[]):
        self.users = users
        self.pending_sessions = pending_sessions
        self.active_sessions = active_sessions

        ## Initiate clean up background task

    # Creates a robot user and adds them to players, returns robot_id, robot_name
    # def add_bot_to_session()

    def handle_session(self, socketio : SocketIO, session_id : int, session_room : str):
        print(f"Handling session {session_id}...")
        
        # robot_user_id, robot_name = self.add_bot_to_session(session_id=session_id, socketio=socketio, delay=random.randint(2,6))
        with db_session() as db:
            tmp_session = db.query(SessionModel).filter_by(id=session_id).one_or_none()
            while not tmp_session.robot_id:
                socketio.sleep(1)
                db.refresh(tmp_session)
                print(tmp_session.robot_id)
            robot_user = db.query(UserModel).filter_by(id=tmp_session.robot_id).one_or_none()
            robot_name = robot_user.username
            robot_user_id = robot_user.id

        #Starting message
        send_server_message_with_delay(sockio=socketio, session_id=session_id, room=session_room, message="Session is starting in 5s...", delay=5)
        socketio.sleep(5)
        
        #Main game loop, While session is ACTIVE, manager performs game operations(i.e read messages, query gpt, parse reponses).
        robot = RobotController(RobotType.gpt4, robot_name=robot_name)

        ## Run a round, rounds are indexed starting at 1##
        ##########################################################################################################################################
        current_round = 1
        current_state = self.get_session_status(session_id=session_id)
        number_of_rounds = SessionManager.MIN_HUMAN_PLAYERS_NEEDED
        self.get_active_player_count
        while current_round <= number_of_rounds: #[1, number_of_rounds+1)
            send_server_message_with_delay(sockio=socketio, session_id=session_id, room=session_room, message=f"Starting round {current_round}. There is a bot among you...")
            start_time = time.time()
            emit_message(sockio=socketio, action='round_start', room=session_room, data={"round" : current_round , "time" : SessionManager.MAX_TIME}, delay=0)

            while current_state == SessionState.ACTIVE:
                # Elapsed time 2 minutes?
                elapsed_time = time.time() - start_time
                if  elapsed_time >= SessionManager.MAX_TIME:
                    break

                with db_session() as db:
                    current_session = db.query(SessionModel).filter_by(id=session_id).one_or_none()
                    current_state = current_session.state

                    # Reasons to end game here
                    if not current_session or not current_session.enough_players():# Not enough players to continue(need min 2 person and AI)
                        break
                
                socketio.sleep(random.randint(3,8))

                try:
                    ai_response = robot.get_response(session_id=session_id)
                    if ai_response:
                        ai_response_json = json.loads(ai_response)
                        if "message" in ai_response_json:
                            send_message_with_delay(sockio=socketio, sender_name=ai_response_json['from'].strip("'"), session_id=session_id, room=session_room, message=ai_response_json['message'])
                except Exception as e:
                    print(e)
                    
            emit_message(sockio=socketio, action='round_end', room=session_room, data={"round" : current_round}, delay=0)
            send_server_message_with_delay(sockio=socketio, session_id=session_id, room=session_room, message=f"<h1>Round {current_round} finished!</h1><span>chat disabled</span>")
            ##########################################################################################################################################

            # clients will trigger ("submit_vote")
            ## Conduct Voting for said round##
                ## Trigger voting action for socketio
            with db_session() as db:
                tmp_session = db.query(SessionModel).filter_by(id=session_id).one_or_none()
                if(tmp_session):
                    tmp_session.state = SessionState.INACTIVE

            with db_session() as db:
                tmp_session = db.query(SessionModel).filter_by(id=session_id).one_or_none()
                active_players = []
                for p in tmp_session.players:
                    if p.state == UserState.ACTIVE:
                        active_players.append(p.to_dict())
                emit_message(sockio=socketio, action="begin_vote", room=session_room, data={'begin_voting' : True, "round" : current_round, "users" : active_players, "time" : SessionManager.VOTE_TIME})
                socketio.sleep(SessionManager.VOTE_TIME)
                emit_message(sockio=socketio, action="stop_vote", room=session_room, data={'stop_voting' : True, "round" : current_round})

                majority_vote = self.calculate_votes(session_id=session_id, round_number=current_round)
                if majority_vote:
                    user_to_kick = db.query(UserModel).filter_by(id=majority_vote['id']).one_or_none()
                    user_to_kick.state = UserState.VOTED_OUT
                    db.flush()

                    send_server_message_with_delay(sockio=socketio, session_id=session_id, room=session_room, message=f"{user_to_kick.username} has been voted out!")

                    if majority_vote['id'] == tmp_session.robot_id:
                        #humans_win_handler
                        send_server_message_with_delay(sockio=socketio, session_id=session_id, room=session_room, message=f"<h1>The AI has been identified, Humans win!👩🏻‍🤝‍👨🏾</h1>", delay=5)
                        break # exit session
                else:
                    send_server_message_with_delay(sockio=socketio, session_id=session_id, room=session_room, message=f"no one was voted out...")

                    
                    
                active_player_count = self.get_active_player_count(session_id=session_id)
                if active_player_count > SessionManager.MAX_HUMAN_PLAYERS:
                    current_round = current_round - 1
                    send_server_message_with_delay(sockio=socketio, session_id=session_id, room=session_room, message=f"<h1>The AI lives on...</h1>", delay=5)
                elif active_player_count <= SessionManager.MAX_HUMAN_PLAYERS or current_round == number_of_rounds:
                    ascii_art = """
                    (arrowhead)	⤜(ⱺ ʖ̯ⱺ)⤏
                    (apple)	
                    (ass)
                    (butt)	(‿|‿)
                    (awkward)	•͡˘㇁•͡˘
                    (bat)	/|\ ^._.^ /|\
                    (bear)
                    (koala)	ʕ·͡ᴥ·ʔ
                    (bearflip)	ʕノ•ᴥ•ʔノ ︵ ┻━┻
                    (bearhug)	ʕっ•ᴥ•ʔっ
                    """
                    evil_message = robot.simple_ask(f"You are a chat bot that has been pretending to be human this whole time. Generate a 2-5 word message claiming your victory over the human losers hehe or just use a ascii art like the following: {ascii_art}")
                    send_message_with_delay(sockio=socketio, sender_name=robot.get_robot_name(session_id=session_id), session_id=session_id, room=session_room, message=evil_message, delay=5)
                    send_server_message_with_delay(sockio=socketio, session_id=session_id, room=session_room, message="<h1>AI Wins 🤖</h1>")
                    break

            current_round += 1


            



            ## Collect casted votes, if connection issues, player vote not counted
            ## Determine who gets voted out
            ## Determine if players or AI wins




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
                
            new_pending_session = SessionModel(room=room, max_players_allowed=SessionManager.MAX_HUMAN_PLAYERS)
            db.add(new_pending_session)
            db.commit()
            
            self.add_user(session_id=new_pending_session.id, user_id=host_id, sock=sock)
            sock.start_background_task(self.add_bot_to_room, new_pending_session.room, sock, random.randint(5, 20))

            return new_pending_session.room, f"New game session created, {room}."


    def join_session(self, user_id, room="", random_room=False, sock: SocketIO = None, is_bot = False):
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

                self.add_user(session_id=current_session.id, user_id=current_user.id, sock=sock, is_bot=is_bot)
                #db.add(current_session)
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
                #send_message_with_delay(sockio=socketio, sender_name="Server", session_id=session_id, room=tmp_session.room, message=f"Session has ended...", delay=5)
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
            tmp_session = db.query(SessionModel).filter_by(id=session_id).one_or_none()
            if tmp_session:
                return tmp_session.state
            return None
    
    def get_player_dict(self, session_id):
        with db_session() as db:
            tmp_session = db.query(SessionModel).filter_by(id=session_id).one_or_none()
            if tmp_session:
                return [p.to_dict() for p in tmp_session.players]
            return None

    def set_session_status(self, session_id: int, new_status: SessionState):
        with db_session() as db:
            curr_session = db.query(SessionModel).filter_by(id=session_id).one_or_none()
            if curr_session:
                curr_session.state = new_status

    def add_user(self, session_id : int, user_id : int, sock : SocketIO, is_bot = False):
        with db_session() as db:
            user = db.query(UserModel).filter_by(id=user_id).one()
            tmp_session = db.query(SessionModel).filter_by(id=session_id).one()

            room_for_more_players = tmp_session.get_user_count() <= tmp_session.max_players_allowed
            player_not_active = user.state != UserState.ACTIVE
            session_pending = tmp_session.state == SessionState.PENDING

            if session_pending and player_not_active and (room_for_more_players or is_bot):
                if not tmp_session.host_id: # AI can be host
                    tmp_session.set_host(user.id)
                
                if is_bot:
                    tmp_session.set_bot(user_id)
                
                user.state = UserState.ACTIVE
                tmp_session.players.append(user)
                user.session_id = tmp_session.id

                db.flush()

                if tmp_session.get_user_count() > tmp_session.max_players_allowed: # >(not inclusive) for AI
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
            
    def handle_vote(self, user_id : int, session_id : int, round : int, voted_id : int, on_complete = None):
        with db_session() as db:
            tmp_session = db.query(SessionModel).filter_by(id=session_id).one_or_none()

            if tmp_session and tmp_session.state == SessionState.INACTIVE:
                #If vote array exits, update current set current round to vote

                #
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
                    size = len(tmp_session.players) - 1 # Minus 1 for AI, for example 4 human players and 1 AI is 3 rounds.
                    new_votes_per_round = [None] * (size if size >= 1 else 1)  # Create a list with 'None' for past rounds
                    new_votes_per_round[round - 1] = voted_id
                    
                        # Insert the new vote entry
                    vote_entry = session_votes.insert().values(session_id=session_id, user_id=user_id, user_voted_per_round=new_votes_per_round)
                    db.execute(vote_entry)
                
                print(f"User(id: {user_id}) submitted vote!")

            if on_complete:
                on_complete()

    

    #  Count the votes of Session(id=session_id, round=round_number) and if there is majority, return user_id else none
    def calculate_votes(self, session_id : int, round_number : int):
        with db_session() as db:
            tmp_session = db.query(SessionModel).filter_by(id=session_id).one_or_none()
            if not tmp_session:
                print(f"session_id:{session_id} is not a valid session")
                return

            half_of_player_size = (len(tmp_session.players)-1) / 2 # Not counting AI vote
            votes_counted = {} # user_id : votes

            for user in tmp_session.players:
                if user.id == tmp_session.robot_id:
                    print("robots can't vote...yet")
                    continue

                try:
                    vote_entry = db.query(session_votes).filter_by(session_id=session_id, user_id=user.id).one_or_none()
                    if (vote_entry):
                        user_voted_per_round = vote_entry.user_voted_per_round
                        possible_id = user_voted_per_round[round_number - 1] # Round number 1 conisides with index the first index, 0.
                        user_voted = db.query(UserModel).filter_by(id=possible_id).one()

                        if user_voted.id not in votes_counted:
                            votes_counted[user_voted.id] = 1
                        else:
                            votes_counted[user_voted.id] += 1

                        print(f"{user.username} voted for {user_voted.username}")
                    else:
                        print(f"{user.username} didn't vote")

                except NoResultFound:
                    print(f"calculate_vote could not find user with id {possible_id}")

            # key defines a lambda that takes in x which is an elem from votes_counted.items() and returns the value to compare.
            if not votes_counted:
                return None
            max_vote = {'id' : None, 'count' : None}
            tmp_vote = max(votes_counted.items(), key=lambda x: x[1])

            max_vote['id'] = tmp_vote[0]
            max_vote['count'] = tmp_vote[1]

            if max_vote['count'] > half_of_player_size: # majority
                return max_vote
            else:
                return None
    
    def get_active_player_count(self, session_id):
        with db_session() as db:
            tmp_session = db.query(SessionModel).filter_by(id=session_id).one_or_none()
            if tmp_session:
                active_player_count = 0
                for player in tmp_session.players:
                    if player.id != tmp_session.robot_id and player.state != UserState.VOTED_OUT:
                        active_player_count += 1
                return active_player_count
        return None


    def add_bot_to_room(self, room : str, socketio : SocketIO = None, delay = 0):
        #Generate robot user id here
        with db_session() as db:
            robot_name = RobotController.simple_ask(ask="Generate a simple cool username like 'notabot' or 'smoot'")
            robot_user = UserModel(username=robot_name)
            db.add(robot_user)
            db.commit()


            socketio.sleep(delay)
            self.join_session(user_id=robot_user.id, room=room, sock=socketio, is_bot=True)
            tmp_session = db.query(SessionModel).filter_by(room=room).one_or_none()
            if tmp_session:
                user_num = len(self.get_player_dict(session_id=tmp_session.id))
                tmp_msg = send_server_message_with_delay(sockio=socketio, session_id=None, room=tmp_session.room, message=f'user {user_num}/{SessionManager.MAX_HUMAN_PLAYERS + 1} joined!')

                tmp_session.messages.append(tmp_msg)

