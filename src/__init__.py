from flask import Flask, session, redirect
from flask_socketio import SocketIO
from flask_cors import CORS

from src.manager import SessionManager



app = Flask(__name__)
socketio = SocketIO()
session_manager = SessionManager()
CORS(app, origins=["http://localhost:5000", "http://127.0.0.1:8081", "http://10.0.0.54:8081"], supports_credentials=True, resources={r"/*": {"origins": "*"}})

def create_app(debug=False):
	"""Create an application."""
	app.config.from_mapping(
		SECRET_KEY = "0349u,qgf[p0jtfp4903e[uj",
		DEBUG = debug,		
	)
	
	from .home import bp as home_blueprint
	app.register_blueprint(home_blueprint)

	from .chat import bp as chat_blueprint
	app.register_blueprint(chat_blueprint)

	from .api import bp as api_blueprint
	app.register_blueprint(api_blueprint)


	socketio.init_app(app)


	return app
