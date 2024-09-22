import os

from flask import Blueprint, session, request, jsonify, Response
from http import HTTPStatus

from src import session_manager, socketio
from src.user import User
from src.session import Session
from src.utils import is_registered


bp = Blueprint("api", __name__, url_prefix="/api")
ws_url = os.getenv("WS_URL")
MAX_USERNAME_SIZE = 30



@bp.route("/")
def index():
    return jsonify(message="Chat API is running"), HTTPStatus.OK


@bp.route("/lobby", methods=["GET", "POST"])
@is_registered
def lobby():
    current_user : User = session_manager.users[session['user']]

    if request.method == "POST":
        if request.json.get("type") == "join":
            # Handle join request

            result = False
            msg = ""
            room = ""
            curr_sesh  : Session = None
            if request.json.get("random"):
                result, msg, curr_sesh  = session_manager.join_session(username=current_user.username, random_room=True)
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
                result, msg, curr_sesh = session_manager.join_session(username=current_user.username, room=room)
                
            if result:
                current_user.session = curr_sesh
                return (
                    jsonify(
                        message=msg,
                        data={"room": curr_sesh.room},
                        did_succeed=True,
                        ws=ws_url

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
            result, msg, curr_sesh = session_manager.create_session(host=current_user.username, room=room, sock=socketio)
            if(result):
                current_user.session = curr_sesh
                return (
                    jsonify(
                        message=msg,
                        data={"room": curr_sesh.room},
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
                 
    return (
        jsonify(message=f"Welcome {current_user.username}!", data={"user": current_user.to_dict()}),
        HTTPStatus.OK,
    )


@bp.route("/lobby/sessions", methods=["GET"])
def list_lobby():
    pending_games = [s.to_dict() for s in session_manager.pending_sessions]
    active_games = [s.to_dict() for s in session_manager.active_sessions]
    return (
        jsonify(
            message=f"Game sessions",
            pending_sessions=pending_games,
            active_sessions=active_games
        ),
        HTTPStatus.OK,
    )

@bp.route("/lobby/users", methods=["GET"])
def list_users():
    user_dicts = [v.to_dict() for v in session_manager.users.values()]
    print(user_dicts)
    return (
        jsonify(
            message="Registered users",
            users=user_dicts,
        ),
        HTTPStatus.OK,
    )

@bp.route("/register", methods=["POST"])
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
    
    if username not in session_manager.users:
        session["user"] = username
        tmp_user = User(session["user"])
        session_manager.add_user(tmp_user)

        print("User registered:", tmp_user.to_dict())
        return (
            jsonify(
                did_succeed=True,
                message=f"Registration Success!",
                data={"user": tmp_user.username}
            ),
            HTTPStatus.OK,
        )

        # TODO Maybe return similar names to originall typed name
    return jsonify(did_succeed=False, message=f"User already exists"), HTTPStatus.OK


@bp.route("/logout")
@is_registered
def logout():
    username = session.pop("user")
    user : User = session_manager.users.pop(username)
    user.disconnect()
    return jsonify(message=f"Logout successful. Adios, pal."), HTTPStatus.OK


