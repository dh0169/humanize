import json

from flask import Blueprint, session, request, jsonify, Response
from functools import wraps
from src.utils import is_registered
from http import HTTPStatus

from src import session_manager
from src.user import User


bp = Blueprint("api", __name__, url_prefix="/api")

MAX_USERNAME_SIZE = 30

def is_reg(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user" not in session:
            return jsonify(did_succeed=False, message="Please register a username"), 401
        elif session["user"] not in session_manager.users:
            return jsonify(did_succeed=False, message="Please register a username"), 401
        return f(*args, **kwargs)

    return decorated_function


@bp.route("/")
def index():
    return jsonify(message="Chat API is running"), HTTPStatus.OK

# Lobby group


@bp.route("/lobby", methods=["GET", "POST"])
@is_reg
def lobby():
    current_user : User = session_manager.users[session['user']]

    if request.method == "POST":
        if request.json.get("type") == "join":
            # Handle join request

            result = False
            msg = ""
            room = ""
            if request.json.get("random"):
                result, msg = session_manager.join_session(username=current_user.username, random_room=True)
            else:
                room = request.json.get("room")
                if not room or type(room) is not str:
                    return (
                    jsonify(
                        did_succeed=False,
                        message=f"room cannot be empty or null",
                    ),
                    HTTPStatus.BAD_REQUEST,
                )
                result, msg = session_manager.join_session(username=current_user.username, room=room)
                
            if not room:
                room = "random" 
            if result:
                return (
                    jsonify(
                        message=msg,
                        data={"room": room},
                        did_succeed=True,
                        socketio="http://localhost:5000/chat"

                    ),
                    HTTPStatus.OK,
                )
            else:
                return (
                    jsonify(
                        message=msg,
                        data={"room": room},
                        did_succeed=False
                    ),
                    HTTPStatus.OK,
                )
        elif request.json.get("type") == "host":
            # Handle host request
            room = request.json.get("room")
            if not room:
                return (
                    jsonify(
                        did_succeed=False,
                        message=f"room cannot be empty or null",
                    ),
                    HTTPStatus.BAD_REQUEST,
                )
            result, msg = session_manager.create_session(host=current_user.username, room=room)
            if(result):
                return (
                    jsonify(
                        message=msg,
                        data={"session": session},
                        did_succeed=True
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
                 
    return (
        jsonify(message=f"Welcome {current_user.username}!", data={"user": current_user.to_dict()}),
        HTTPStatus.OK,
    )


@bp.route("/lobby/sessions", methods=["GET"])
@is_reg
def list_lobby():
    pending_games = [s.to_dict() for s in session_manager.pending_sessions]
    active_games = [s.to_dict() for s in session_manager.active_sessions]
    return (
        jsonify(
            message=f"Sessions available to join",
            pending_sessions=pending_games,
            active_sessions=active_games
        ),
        HTTPStatus.OK,
    )

@bp.route("/lobby/users", methods=["GET"])
@is_reg
def list_users():
    user_dicts = [u.to_dict() for u in session_manager.users.values()]
    return (
        jsonify(
            message="Users in game",
            users=user_dicts,
        ),
        HTTPStatus.OK,
    )

@bp.route("/register", methods=["POST"])
def register():
    username = request.json["username"]
    if username not in session_manager.users:
        session["user"] = username[:MAX_USERNAME_SIZE]
        tmp_user = User(session["user"])
        session_manager.add_user(tmp_user)
        print(tmp_user.to_dict())
        return (
            jsonify(
                did_succeed=True,
                message=f"Registration Success!",
                data={"user": session["user"]},
            ),
            HTTPStatus.OK,
        )

        # TODO Maybe return similar names to originall typed name
    return jsonify(did_succeed=False, message=f"User already exists"), HTTPStatus.OK


@bp.route("/logout")
def logout():
    if "user" in session:
        username = session.pop("user")
        if username in session_manager.users:
            session_manager.users.pop(username)
        return jsonify(message=f"Logout successful. Adios, pal."), HTTPStatus.OK
    return jsonify(message=f"No session found"), HTTPStatus.OK


