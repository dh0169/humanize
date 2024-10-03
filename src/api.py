import os
from src import session_manager, socketio
from src.utils import is_registered, handle_db_errors
from src.models import db_session, UserModel, SessionModel, SessionState
from flask import Blueprint, session, request, jsonify, Response
from sqlalchemy import select
from http import HTTPStatus

bp = Blueprint("api", __name__, url_prefix="/api")
ws_url = os.getenv("WS_URL")
MAX_USERNAME_SIZE = 30



@bp.route("/")
def index():
    return jsonify(message="Chat API is running"), HTTPStatus.OK


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
                if not room or type(room) is not str:
                    return (
                    jsonify(
                        did_succeed=False,
                        message=f"room cannot be empty or null",
                    ),
                    HTTPStatus.BAD_REQUEST,
                )
                room_joined, msg = session_manager.join_session(user_id=user_id, room=room, sock=socketio)
                
            if room_joined:
                return (
                    jsonify(
                        message=msg,
                        data={"room": room_joined},
                        did_succeed=True,
                        ws=ws_url

                    ),
                    HTTPStatus.OK,
                )
            else:
                return (
                    jsonify(
                        message=msg,
                        did_succeed=False
                    ),
                    HTTPStatus.OK,
                )
        elif request.json.get("type") == "host":
            # Handle host request
            if not room:
                return (
                    jsonify(
                        did_succeed=False,
                        message=f"room cannot be empty or null",
                    ),
                    HTTPStatus.BAD_REQUEST,
                )
            room_joined, msg = session_manager.create_session(host_id=user_id, room=room, sock=socketio)
            if(room_joined):
                return (
                    jsonify(
                        message=msg,
                        data={"room": room_joined},
                        did_succeed=True,
                        ws=ws_url
                    ),
                    HTTPStatus.OK,
                )
            else:
                return (
                    jsonify(
                        message=msg,
                        did_succeed=False
                    ),
                    HTTPStatus.OK,
                )
    with db_session() as db:
        current_user = db.query(UserModel).filter_by(id=user_id).one()
        return (
            jsonify(message=f"Welcome {current_user.username}!", data={"user": current_user.to_dict()}),
            HTTPStatus.OK,
        )


@bp.route("/lobby/sessions", methods=["GET"])
@handle_db_errors
def list_lobby():
    with db_session() as db:
        pending_games = [gs.to_dict() for gs in db.query(SessionModel).filter_by(state=SessionState.PENDING).all()]
        active_games = [gs.to_dict() for gs in db.query(SessionModel).filter_by(state=SessionState.ACTIVE).all()]

        return (
            jsonify(
                message=f"Game sessions",
                pending_sessions=pending_games,
                active_sessions=active_games
            ),
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
            jsonify(
                message="Registered users",
                users=user_dicts,
            ),
            HTTPStatus.OK,
        )


@bp.route("/register", methods=["POST"])
@handle_db_errors
def register():
    username : str = request.json["username"]
    if not username.isalnum() or len(username) > 30:
        return (
            jsonify(
                did_succeed=False,
                message=f"username must be a max 30 characters, alpha numeric only.",
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
                    did_succeed=True,
                    message=f"Registration Success!",
                    data={"user": tmp_user.username}
                ),
                HTTPStatus.OK,
            )
        
        else:
            return jsonify(did_succeed=False, message=f"User already exists"), HTTPStatus.OK




@bp.route("/logout")
@is_registered
@handle_db_errors
def logout():
    user_id = session["user"]
    session_manager.disconnect_player(user_id=user_id)
    if "user" in session:
        session.pop("user")
    return jsonify(message=f"Logout successful. Adios, pal."), HTTPStatus.OK


