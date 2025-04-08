import os
from src import session_manager, socketio
from src.utils import is_registered, handle_db_errors
from src.models import db_session, UserModel, SessionModel, SessionState
from flask import Blueprint, session, request, jsonify
from src.config import WS_URL
from http import HTTPStatus
from copy import deepcopy

bp = Blueprint("api", __name__, url_prefix="/api", )
MAX_USERNAME_SIZE = 30


@bp.route("/")
def index():
    return jsonify(status='ok', message='Hi there:)'), HTTPStatus.OK


@bp.route("/lobby", methods=["GET", "POST"])
@is_registered
@handle_db_errors
def lobby():
    user_id = session['user']

    if request.method == "POST":
        msg = ""
        room_joined = None
        room = request.json.get("room")
        
        if request.json.get("type") == "join":
            # Handle join request

            if request.json.get("random"):
                room_joined, msg  = session_manager.join_session(user_id=user_id, random_room=True, sock=socketio)
            else:
                if not room:
                    return (
                    jsonify(
                        status='error',
                        message="room cannot be empty or null",
                    ),
                    HTTPStatus.OK,
                )
                
                if type(room) is not str:
                    return (
                    jsonify(
                        status='error',
                        message="room must be a string",
                    ),
                    HTTPStatus.OK,
                )
                room_joined, msg = session_manager.join_session(user_id=user_id, room=room, sock=socketio)
                
            if room_joined:
                content = {
                    "room": room_joined,
                    "ws":WS_URL
                }
                return ( 
                    jsonify(status='ok', message=msg, content=content),
                    HTTPStatus.OK,
                )
            else:
                return (
                    jsonify(
                        message=msg,
                        status='error'
                    ),
                    HTTPStatus.OK,
                )
        elif request.json.get("type") == "host":
            # Handle host request
            if not room:
                return (
                    jsonify(
                        status='error',
                        message="room cannot be empty or null",
                    ),
                    HTTPStatus.BAD_REQUEST,
                )
            room_joined, msg = session_manager.create_session(host_id=user_id, room=room, sock=socketio)
            if(room_joined):
                content = {
                    "room": room_joined,
                    "ws":WS_URL
                }
                return ( 
                    jsonify(status='ok', message=msg, content=content),
                    HTTPStatus.OK,
                )
            else:
                return (
                    jsonify(
                        message=msg,
                        status='error'
                    ),
                    HTTPStatus.OK,
                )
    with db_session() as db:
        current_user = db.query(UserModel).filter_by(id=user_id).one()
        return (
            jsonify(status='ok', message=f"Welcome {current_user.username}!", content={"user": current_user.to_dict()}),
            HTTPStatus.OK,
        )


@bp.route("/lobby/sessions", methods=["GET"])
@handle_db_errors
def list_lobby():
    with db_session() as db:
        pending_games = [gs.to_dict() for gs in db.query(SessionModel).filter_by(state=SessionState.PENDING).all()]
        active_games = [gs.to_dict() for gs in db.query(SessionModel).filter_by(state=SessionState.ACTIVE).all()]

        content = {
            'pending_sessions' : pending_games,
            'active_sessions' : active_games
        }
        return (
            jsonify(status='ok', message='Available sessions', content=content),
            HTTPStatus.OK,
        )
    
@bp.route("/lobby/sessions/<sesh_id>", methods=["GET"])
@handle_db_errors
def get_sess_by_id(sesh_id):
    with db_session() as db:
        tmp_sesh = db.query(SessionModel).filter_by(id=sesh_id).one_or_none()        
        return (
            jsonify(status='ok', message='Available sessions', content=tmp_sesh.to_dict() if tmp_sesh else None),
            HTTPStatus.OK,
        )


@bp.route("/lobby/users", methods=["GET"])
@handle_db_errors
def list_users():
    user_dicts = []
    with db_session() as db:
        users = db.query(UserModel).all()
        user_dicts = [u.to_dict() for u in users]
        return ( 
            jsonify(status='ok', message='Registered users', content=user_dicts),
            HTTPStatus.OK,
        )


@bp.route("/register", methods=["POST"])
@handle_db_errors
def register():
    username : str = request.json["username"]
    if not username.isalnum() or len(username) > 30:
        return (
            jsonify(
                status='error',
                message="username must be a max 30 characters, alpha numeric only.",
            ),
            HTTPStatus.OK,
        )
    
    with db_session() as db:
        tmp_user = db.query(UserModel).filter_by(username=username).one_or_none()
        if not tmp_user:
            tmp_user = UserModel(username=username)             
            db.add(tmp_user)
            db.flush() #Send pending changes to db so that we can get id number, autoassigned primary key
            
            session["user"] = tmp_user.id



            print("User registered:", tmp_user.to_dict())
            return (
                jsonify(
                    status='ok',
                    message=f"Registration Success!",
                    content={"user": tmp_user.username}
                ),
                HTTPStatus.OK,
            )
        
        else:
            return jsonify(status='error', message=f"User already exists"), HTTPStatus.OK




@bp.route("/logout")
@is_registered
@handle_db_errors
def logout():
    user_id = session["user"]
    session_manager.disconnect_player(user_id=user_id)
    if "user" in session:
        session.pop("user")
    return jsonify(status='ok', message=f"Logout successful. Adios, pal."), HTTPStatus.OK


