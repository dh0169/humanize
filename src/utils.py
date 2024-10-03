from functools import wraps
from flask import session, jsonify, current_app
from flask_socketio import SocketIO
from sqlalchemy.exc import NoResultFound, SQLAlchemyError
from http import HTTPStatus
from src.models import db_session, UserModel, MessageModel

from datetime import datetime



def is_registered(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            with db_session() as db:
                if "user" not in session :
                    return jsonify(did_succeed=False, message="Please register a username"), HTTPStatus.UNAUTHORIZED
                db.query(UserModel).filter_by(id=session["user"]).one()

            return f(*args, **kwargs)
        except NoResultFound as e:
            return jsonify(did_succeed=False, message="Please register a username"), HTTPStatus.UNAUTHORIZED        

    return decorated_function

def handle_db_errors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except SQLAlchemyError as e:
            print(e)
            return jsonify(message="A database error occurred"), HTTPStatus.INTERNAL_SERVER_ERROR
        except Exception as e:
            print(e)
            return jsonify(message="An unexpected error occurred"), HTTPStatus.INTERNAL_SERVER_ERROR
    return wrapper

def send_message(sockio : SocketIO, sender_name : str, session_id : int, room : str, message : str, include_self : bool = True):
    tmp_msg = MessageModel(sender=sender_name, session_id=session_id, message=message, timestamp=datetime.now())
    if room:
        sockio.send(tmp_msg.to_dict(), to=room, namespace="/chat", include_self=include_self)
    else:
        sockio.send(tmp_msg.to_dict(), namespace="/chat", include_self=include_self)
        
    return tmp_msg
    

def send_message_with_delay(sockio : SocketIO, sender_name : str, session_id : int, room : str, message : str, delay : int = 1, include_self=True):
    sockio.sleep(delay)
    return send_message(sockio=sockio, sender_name=sender_name, session_id=session_id, room=room, message=message, include_self=include_self)


def send_server_message_with_delay(sockio : SocketIO, session_id : int, room : str, message : str, delay : int = 1):
    return send_message_with_delay(sockio=sockio, sender_name="Server", session_id=session_id, room=room, message=message, include_self=True, delay=delay)

