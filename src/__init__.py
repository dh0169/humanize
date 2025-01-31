import eventlet
eventlet.monkey_patch(socket=False) # Need this or openAI fails

from dotenv import load_dotenv, find_dotenv
env_path = find_dotenv()
if not env_path:
	raise FileNotFoundError(".env file not found.")
load_dotenv(env_path)


from flask import Flask, redirect

from flask_socketio import SocketIO
from flask_cors import CORS
from src.manager import SessionManager
from src.config import HUMANIZE_ADMIN, HUMANIZE_ADMIN_PW, HUMANIZE_USER, HUMANIZE_USER_PW, FLASK_SECRET_KEY
from src.models import db_session, SessionModel, UserModel, UserState

from flask_httpauth import HTTPBasicAuth
from werkzeug.security import check_password_hash, generate_password_hash

socketio = SocketIO(cors_allowed_origins="*")
session_manager = SessionManager()


def create_app(debug=False):
	"""Create an application."""

	app = Flask(__name__)

	app.config.from_mapping(
		SECRET_KEY = FLASK_SECRET_KEY,
		DEBUG = debug,
		SESSION_COOKIE_SAMESITE='lax',   # Allows cross-site cookies
		#SESSION_COOKIE_SECURE=True,  
	)
	
	

	from .home import bp as home_blueprint
	app.register_blueprint(home_blueprint)

	from .chat import bp as chat_blueprint
	app.register_blueprint(chat_blueprint)

	from .api import bp as api_blueprint
	app.register_blueprint(api_blueprint)
	
	@app.errorhandler(404)
	def not_found(e):
		return redirect("/")


	with db_session() as db:
		db.query(SessionModel).delete()
		db.query(UserModel).update({ UserModel.state : UserState.WAITING})
	

	CORS(app, supports_credentials=True, origins=['http://localhost:3000', 'http://127.0.0.1:3000'])
	
	socketio.init_app(app, async_model="eventlet")

	return app
