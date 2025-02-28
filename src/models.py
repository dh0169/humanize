import enum, random

from datetime import datetime
from contextlib import contextmanager
from sqlalchemy import Column, Integer, String, Enum, ForeignKey, Table, DateTime, JSON, create_engine 
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session, relationship

from src.config import DATABASE_URI
Base = declarative_base()


# How to use database:
# 
#       from src.models import UserModel, SessionModel, UserState, SessionState, db_session       
#
#       with db_session() as db:
#           tmp_sessions = db.query(SessionModel).all() # returns all session objects
#           tmp_user = db.query(UserModel).filter_by(id=user_id).one_or_none() # returns the object or None
#           
#           CRUD operations on db object must happen within the db session. 
#           Cant pass object around as its tied to db sesh. 


def delete_by_id(id, model, delay = 0, sock = None):
    with db_session() as db:
        robot_user = db.query(model).filter_by(id=id).one_or_none()
        if robot_user:
            if sock:
                sock.sleep(delay)
            db.delete(robot_user)


def get_db():
    engine = create_engine(DATABASE_URI)
    SessionFactory = sessionmaker(bind=engine)
    Base.metadata.create_all(engine)
    return scoped_session(SessionFactory)
    

@contextmanager
def db_session():
    session = get_db()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()



player_sessions = Table(
    'player_sessions', Base.metadata,
    Column('session_id', Integer, ForeignKey('sessions.id'), primary_key=True),
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True)
)

session_votes = Table(
    'session_votes', Base.metadata,
    Column('session_id', Integer, ForeignKey('sessions.id'), primary_key=True),
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('user_voted_per_round', JSON, nullable=True) # user_id voted off user_voted
)



class MessageModel(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    sender= Column(String, ForeignKey('users.username'))
    session_id = Column(Integer, ForeignKey('sessions.id'))
    message = Column(String, nullable=False)
    timestamp = Column(DateTime(timezone=True), nullable=False)

    
    def __init__(self, sender : str, session_id : int, message : str , timestamp : datetime):
        self.sender = sender
        self.session_id = session_id
        self.message = message
        self.timestamp = timestamp

    def __repr__(self):
        return (f"<Message(id={self.id}, sender={self.sender}, "
                f"session_id={self.session_id}, content={self.message})>")
    
    def to_dict(self):
        tmp_dict = {
            "session" : self.session_id,
            "from" : self.sender,
            "message" : self.message,
            "timestamp" : self.timestamp.strftime("%I:%M%p").lower(),
        }
        return tmp_dict


class UserState(enum.Enum):
    DISCONNECTED = -1
    WAITING = 0
    ACTIVE = 1
    VOTED_OUT = 2

class UserModel(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(30), nullable=False)
    session_id = Column(Integer, ForeignKey('sessions.id'))
    state = Column(Enum(UserState), default=UserState.WAITING, nullable=False)

    
    def __init__(self, username: str, state: UserState = UserState.WAITING):
        self.username = username
        self.state = state

    def __repr__(self):
        return (f"<User(id={self.id}, username={self.username!r}, "
                f"session_id={self.session_id}, state={self.state})>")

    def to_dict(self):
        r = {
            'id' : self.id,
            'username': self.username,
            'state': self.state.name,  # Use the name of the enum
        }
        if self.session_id:
            r['session_id'] = self.session_id 
        return r
    
    def __eq__(self, value: object) -> bool:
        return self.id == value.id


class SessionState(enum.Enum):
    PENDING = 'PENDING'
    ACTIVE = 'ACTIVE'   
    INACTIVE = 'INACTIVE'

class SessionModel(Base):
    __tablename__ = 'sessions'

    id = Column(Integer, primary_key=True, autoincrement=True) 
    room = Column(String(100), unique=True)                               # Unique Room name
    robot_id = Column(Integer, ForeignKey('users.id'), nullable=True, default=None)               # AI Model Name (i.e gpt-3.5 turbo)
    host_id = Column(Integer, ForeignKey('users.id'), nullable=True)      # User id who is host
    state = Column(Enum(SessionState), default=SessionState.PENDING)      # Session state
    max_players_allowed = Column(Integer, default=4)


    players = relationship("UserModel", secondary=player_sessions)
    messages = relationship("MessageModel", backref="session", cascade="all, delete-orphan")
    votes = relationship("UserModel", secondary=session_votes)



    def __init__(self, room="", robot=None, host_id=None, thread_id=None, state=SessionState.PENDING, max_players_allowed=4, socketio=None):
        self.room = room
        self.robot = robot 
        self.host_id = host_id
        self.thread_id = thread_id
        self.state = state
        self.max_players_allowed = max_players_allowed

    def is_host(self, user_id):
        if self.host_id == user_id:
            return True
        return False
    
    def reassign_host(self):
        if self.players:
            new_host = random.choice(self.players)
            self.set_host(new_host.id)
   

    def set_host(self, host_id):
        self.host_id = host_id

    def set_bot(self, bot_id):
        self.robot_id = bot_id


    def get_user_count(self):
        return len(self.players)
    
    def end_game(self):
        self.__set_state__(SessionState.INACTIVE)

    def is_running(self):
        return self.state == SessionState.ACTIVE   

    def enough_players(self):
        return self.get_user_count() > 1  
    
    def get_state(self):
        return self.state

    def __set_state__(self, state: SessionState):
        self.state = state   

    def start_game(self):
        self.__set_state__(SessionState.ACTIVE)
        
    def end_game(self):
        self.__set_state__(SessionState.INACTIVE)

    def is_running(self):
        return self.state == SessionState.ACTIVE
    

    def __repr__(self):
        # robot={self.robot_id if self.robot_id else None},
        return (f"<Session(id={self.id}, room={self.room!r},  "
                f"host_id={self.host_id}, state={self.state.value!r}, "
                f"max_players_allowed={self.max_players_allowed})>")
    
    def to_dict(self):
        r = {
            'room': self.room,
            'host_id': self.host_id,
            'state': self.state.name,
            'max_players_allowed': self.max_players_allowed,
        }
        if self.players:
            r['players'] = [p.to_dict() for p in self.players]
        else:
            r['players'] = []

        return r

    def __eq__(self, value: object) -> bool:
        return self.room == value.room



