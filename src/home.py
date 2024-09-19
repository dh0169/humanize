from flask import Blueprint, render_template, session, request, jsonify, redirect, url_for
from functools import wraps
from src.chat import active_users
from src.utils import is_registered

bp = Blueprint("home", __name__, url_prefix="/")



@bp.route("/")
def index():
	return render_template("index.html")

@bp.route("/lobby", methods=["GET", "POST"])
@is_registered
def lobby():
	if request.method == "POST":
		print(request.json)

		#Handle `join request

		#Handle host request


	return render_template("lobby.html")

@bp.route("/register", methods=['POST'])
def register():
	username = request.form['username']
	if username and username not in active_users:
		session['user'] = username
		active_users.append(username)
		return redirect(url_for("home.lobby"))

	return redirect("/")
	#jsonify(status=False, msg=f"{username} already active! Please choose different name.")

@bp.route("/active")
def active():
	if 'user' in session:
		print(session['user'])
	return active_users



