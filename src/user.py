import random, enum, base64, json
from src.session import Session

class User():
    class State(enum.Enum):
        DISCONNECTED = -1
        WAITING = 0
        ACTIVE = 1

    def __init__(self, username: str, state: State = State.WAITING, session : Session = None):
        self.username = username
        self.state = state
        self.session = session
    
    def to_dict(self):
        r = {
            'username': self.username,
            'state': self.state.name,  # Use the name of the enum
        }
        if self.session:
            r['session'] = self.session.to_dict()
        return r
    
    def disconnect(self):
        if self.session:
            self.session.disconnect_player(self)
    
    def __eq__(self, value: object) -> bool:
        return self.username == value.username
    
    def to_json(self):
        return json.dumps(self.to_dict())

    @classmethod
    def from_dict(cls, data):
        return cls(
            username=data['username'],
            state=cls.State[data['state']]  # Convert string back to enum
        )

    @classmethod
    def from_json(cls, json_str):
        return cls.from_dict(json.loads(json_str))