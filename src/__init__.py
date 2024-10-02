import eventlet
eventlet.monkey_patch()

from flask import Flask

from flask_socketio import SocketIO
from flask_cors import CORS
from src.manager import SessionManager
from src.config import FLASK_SECRET_KEY




socketio = SocketIO()
session_manager = SessionManager()

def create_app(debug=False):
	"""Create an application."""
	app = Flask(__name__)
	app.config.from_mapping(
		SECRET_KEY = FLASK_SECRET_KEY,
		DEBUG = debug
	)
	
	

	from .home import bp as home_blueprint
	app.register_blueprint(home_blueprint)

	from .chat import bp as chat_blueprint
	app.register_blueprint(chat_blueprint)

	from .api import bp as api_blueprint
	app.register_blueprint(api_blueprint)

	
	CORS(app)
	
	socketio.init_app(app, async_model="eventlet")

	return app
