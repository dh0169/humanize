import random
import enum
import base64
import json
import requests
from src.message import Message


class Session:
    class State(enum.Enum):
        PENDING = 1
        ACTIVE = 0
        INACTIVE = -1

    def __init__(self, room="", robot=None, host=None, state=State.PENDING, max_players_allowed=4, socketio=None):
        self.room = room
        self.players = []
        self.robot = robot
        self.messages = []
        self.host = host
        self.state = state
        self.max_players_allowed = max_players_allowed
        self.waiting_room = None
        self.socketio = socketio

        if host:
            self.waiting_room = "waiting_room_" + base64.b64encode(host.encode('utf-8')).decode('utf-8')
            self.join_room(host)


    def join_room(self, name):
        if name not in self.players and self.state == Session.State.PENDING:
            if not self.host:
                self.set_host(name)

            self.players.append(name)

    def is_host(self, username):
        if self.host and self.host == username:
            return True
        return False
    
    def reassign_host(self):
        if self.players:
            new_host = random.choice(self.players)
            self.host = new_host
        else:
            self.host = ""

    def disconnect_player(self, usr):
        if usr.username in self.players:
            self.players.remove(usr.username)
            usr.session = None
            if self.is_host(usr.username):
                self.reassign_host()
                if self.host:
                    self.socketio.start_background_task(target=self.send_message_with_delay, sender="Server", message=f"{self.host} is the new host.", delay=1)

    def send_message_with_delay(self, sender, message, delay = 5):
        self.socketio.sleep(delay)
        self.send_message(sender=sender, message=message)


    def send_message(self, sender, message):
        msg = Message(sender=sender, message=message, room=self.room)
        self.messages.append(msg)
        self.socketio.emit("message", msg.to_dict(), room=self.room, namespace='/chat')


    def get_state(self):
        return self.state

    def __set_state__(self, state: State):
        self.state = state

    def set_host(self, host):
        self.host = host

    def get_user_count(self):
        return len(self.players)

    def start_game(self):
        self.__set_state__(Session.State.ACTIVE)
        self.socketio.start_background_task(target=self.run_session)
        
    def end_game(self):
        self.__set_state__(Session.State.INACTIVE)

    def is_running(self):
        return self.state == Session.State.ACTIVE   

    def enough_players(self):
        return len(self.players) > 1     


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


    def run_session(self):
        self.send_message_with_delay(sender="Server", message="Game is starting...", delay=1)
        self.send_message_with_delay(sender="Server", message="Some prompt here! Goodluck!", delay=3)
        while self.get_state() == Session.State.ACTIVE:
            curr_user = "AI"

            if not self.enough_players():
                break

            #Player Impersonation Feature
            # if random.randint(1,2) % 2 == 0:
            #     curr_user = random.choice(self.players)

            time_to_think = random.randint(3, 5)
            self.socketio.sleep(time_to_think)
            joke_son = requests.get("https://official-joke-api.appspot.com/random_joke").json()
            self.send_message(curr_user, joke_son["setup"])
            self.socketio.sleep(random.randint(3,5))
            self.send_message(curr_user, joke_son["punchline"])
        
        self.send_message("Server", f"Game over. Closing '{self.room}'.")
        self.socketio.close_room(self.room)
        
