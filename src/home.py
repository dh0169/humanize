from flask import Blueprint, render_template
from flask_httpauth import HTTPBasicAuth
from src.config import FLASK_PW, FLASK_USER
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint("home", __name__, url_prefix="/")
auth = HTTPBasicAuth()

users = {
	FLASK_USER : generate_password_hash(FLASK_PW)
}

@auth.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users.get(username), password):
        return username

@bp.route("/debug")
@auth.login_required
def debug():
	return render_template("debug.html")


@bp.route("/")
def index():
	return render_template("index.html")


