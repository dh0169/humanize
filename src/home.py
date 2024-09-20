from flask import Blueprint, render_template

bp = Blueprint("home", __name__, url_prefix="/")


@bp.route("/debug")
def index():
	return render_template("debug.html")


