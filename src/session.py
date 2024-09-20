import random, enum, base64, json
from flask_socketio import SocketIO
# A session is a game session similar to that of multiplayer games(players join a match, this class represents the match)


# A session will either be created with a host or the first player to join will become host. 
# For now, host does nothing but could lead to some other things in the future


class Session():

    class State(enum.Enum):
        PENDING = 1,
        ACTIVE = 0,
        INACTIVE = -1


    def __init__(self, room="", robot=None, host=None, state=State.PENDING, max_players_allowed=4, sock : SocketIO =None):
        self.room = room
        self.players = []
        self.robot = robot
        self.messages = []
        self.host = host
        self.state = state
        self.max_players_allowed = max_players_allowed
        self.waiting_room = None
        self.sock = sock

        if(host):
            self.waiting_room = "waiting_room_"+base64.b64encode(host.encode('utf-8')).decode('utf-8')
            self.join_room(host)

        if(sock):
            self.send_message({"from" : "Server", "message" : f"Room \"{self.room}\" has be created!"})

# Games need to be PENDING for players to join
    def join_room(self, name):        
        if name not in self.players and self.state == Session.State.PENDING:
            # First player to join a room without a host becomes the host
            if not self.host:
                self.set_host(name)
            
            self.players.append(name)

    def send_message(self, message):
        self.sock.emit("message", {"from" : "Server", "message" : message}, room=self.room)
    
    def send_json(self, obj):
        pass
            
    # Need to reassign host if host leaves
    # def leave_session(self, name):
    #     if name in self.players:
    #         self.players.remove(name)


    def get_state(self):
        return self.state
    
    def __set_state__(self, state : State):
        self.state = state
    
    def set_host(self, host):
        self.host = host


    def get_user_count(self):
        return len(self.players)

    def start_game(self):
        self.send_message("")
        self.__set_state__(Session.State.ACTIVE)
        return
        # gameloop
        while (self.state == Session.State.ACTIVE):
            pass
    
    def end_game(self):
        self.__set_state__(Session.State.INACTIVE)

    def __eq__(self, value: object) -> bool:
        return self.room == value.room
    
    def to_dict(self):
        return {
            'room': self.room,
            'players': self.players,
            'robot': self.robot,
            'host': self.host,
            'state': self.state.name,
            'max_players_allowed': self.max_players_allowed,
            'waiting_room': self.waiting_room
        }

    def to_json(self):
        return json.dumps(self.to_dict())

    @classmethod
    def from_dict(cls, data):
        session = cls(
            room=data['room'],
            robot=data['robot'],
            host=data['host'],
            state=cls.State[data['state']],
            max_players_allowed=data['max_players_allowed']
        )
        session.players = data['players']
        session.messages = data['messages']
        session.waiting_room = data['waiting_room']
        return session

    @classmethod
    def from_json(cls, json_str):
        return cls.from_dict(json.loads(json_str))