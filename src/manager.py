import random, enum
from src.session import Session
from src.user import User

MAX_HUMAN_PLAYERS = 4 

class SessionManager():


    def __init__(self, users = {}, pending_sessions=[], active_sessions=[]):
        self.users = users
        self.pending_sessions = pending_sessions
        self.active_sessions = active_sessions


    #TODO add message to return for example, return False, "Session Active"
    def create_session(self, host="", room=""):
        new_pending_session = Session(host=host, room=room, state=Session.State.PENDING, max_players_allowed=MAX_HUMAN_PLAYERS)
        if new_pending_session in self.pending_sessions or new_pending_session in self.active_sessions:
            return False, "room already exists, please select different room name."
        
        current_user : User = self.users[host]
        if current_user.state == User.State.ACTIVE:
            return False, f"{current_user.username} is already ACTIVE."

        current_user.state = User.State.ACTIVE
        self.pending_sessions.append(new_pending_session)
        #self.session_handler(new_pending_session)

        return True, f"New game session created, {room}."

    def join_session(self, username="", room="", random_room=False):
        if not username:
            return False, "Error, name should not be empty."
        
        if username not in self.users:
            return False, f"{username} not in active users."
            
        current_user : User = self.users[username]

        idx = None

        try:
            if current_user.state == User.State.ACTIVE:
                return False, f"user '{current_user.username}' is already in a session."

            if random_room:
                current_session = random.choice(self.pending_sessions)
            else:
                idx = self.pending_sessions.index(Session(room))
                current_session : Session = self.pending_sessions[idx]


            

            if current_session.get_user_count() < current_session.max_players_allowed:
                current_session.join_room(username)
                current_user.state = User.State.ACTIVE
                
                if current_session.get_user_count() == current_session.max_players_allowed:
                    current_session.start_game()
                
                return True, f"{current_user.username} has joined {current_session.room}!"
            else:
                return False, f"{room} is full!"


        except ValueError:
            return False, f"Error, {room} not found!"
            
            
    def get_pending_sessions(self):
        return self.pending_sessions
        

    def get_active_sessions(self):
        return self.active_sessions

    def add_user(self, user : User):
        if user:
            self.users[user.username] = user
    
    def remove_user(self, username):
        if username in self.users.keys():
            self.users.pop(username)


    # Handles a session after its created
    def session_handler(s : Session):
        pass
