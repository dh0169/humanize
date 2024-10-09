from flask import Blueprint, render_template, session
from flask_httpauth import HTTPBasicAuth
from src.config import FLASK_PW, FLASK_USER, WS_URL
from src.robot import RobotController
from src.models import db_session, UserModel, SessionModel
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint("home", __name__, url_prefix="/")
auth = HTTPBasicAuth()

#if debugging
users = {
	FLASK_USER : generate_password_hash(FLASK_PW)
}

@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users.get(username), password):
        return username
	

@bp.route("/game")
def chat():
    if 'user' in session:
        username = None
        with db_session() as db:
            user = db.query(UserModel).filter_by(id=session['user']).one_or_none()
            if user:
                username = user.username
                if user.session_id:
                    tmp_sess = db.query(SessionModel).filter_by(id=user.session_id).one_or_none()
                    if tmp_sess and tmp_sess.is_running():
                        return render_template("chat.html", username=username, currentRoom=tmp_sess.room, ws_url=WS_URL, placeHolders={"username" : "Enter a name hoe"})
                return render_template("chat.html", username=username, currentRoom=None, placeHolders={"username" : "Enter a name hoe"})
            else:
                 session.pop('user')
    return render_template("chat.html", placeHolders={"username" : "Enter a name hoe"})

@bp.route("/debug")
@auth.login_required
def debug():
	return render_template("debug.html")


@bp.route("/")
def index():
	return render_template("index.html")



