import eventlet

eventlet.monkey_patch(socket=False)  # Need this or openAI fails

from dotenv import load_dotenv, find_dotenv

env_path = find_dotenv()
if not env_path:
    raise FileNotFoundError(".env file not found.")
load_dotenv(env_path)


from flask import Flask, redirect

from flask_socketio import SocketIO
from flask_cors import CORS
from src.manager import SessionManager
from src.config import FLASK_SECRET_KEY, HUMANIZE_ORIGINS
from src.models import db_session, SessionModel, UserModel, UserState

socketio = SocketIO(cors_allowed_origins=HUMANIZE_ORIGINS)
session_manager = SessionManager()


def create_app(debug=False):
    """Create an application."""

    app = Flask(__name__)

    app.config.from_mapping(
        SECRET_KEY=FLASK_SECRET_KEY,
        DEBUG=debug,
        SESSION_COOKIE_SAMESITE="None",  # Allows cross-site cookies
        SESSION_COOKIE_SECURE=True,
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
        db.query(UserModel).update({UserModel.state: UserState.WAITING})

    CORS(
        app,
        supports_credentials=True,
        origin=HUMANIZE_ORIGINS,
    )

    socketio.init_app(app, async_model="eventlet")

    return app
