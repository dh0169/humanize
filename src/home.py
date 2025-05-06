from flask import Blueprint, render_template, session, abort
from src.models import db_session, UserModel, SessionModel
from src.config import auth, WS_URL

bp = Blueprint("home", __name__, url_prefix="/")

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
                        return render_template("chat.html", username=username, currentRoom=tmp_sess.room, ws_url=WS_URL, placeHolders={"username" : "Enter a username..."})
                return render_template("chat.html", username=username, currentRoom=None, placeHolders={"username" : "Enter a name hoe"})
            else:
                 session.pop('user')
    return render_template("chat.html", placeHolders={"username" : "Enter a name..."})

@bp.route("/debug")
#@auth.login_required()
def debug():
    # if auth.current_user() == HUMANIZE_ADMIN:
    return render_template("debug.html")
    # else:
    #      abort(401)



@bp.route("/")
def index():
	return render_template("index.html")



