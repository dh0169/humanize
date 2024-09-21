from datetime import timedelta
from flask import Flask, session, redirect
from flask_socketio import SocketIO
from flask_cors import CORS
from dotenv import load_dotenv

from src.manager import SessionManager
import os


app = Flask(__name__)
socketio = SocketIO()
session_manager = SessionManager()
CORS(app)

def create_app(debug=False):
	"""Create an application."""
	load_dotenv()
	app.config.from_mapping(
		SECRET_KEY = os.getenv("SECRET_KEY"),
		DEBUG = debug
	)
	
	from .home import bp as home_blueprint
	app.register_blueprint(home_blueprint)

	from .chat import bp as chat_blueprint
	app.register_blueprint(chat_blueprint)

	from .api import bp as api_blueprint
	app.register_blueprint(api_blueprint)

	socketio.init_app(app, async_model="eventlet")

	return app
