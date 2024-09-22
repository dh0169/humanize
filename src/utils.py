from functools import wraps
from flask import session, request, redirect, jsonify
from flask_socketio import disconnect
from src import session_manager

def is_registered(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user" not in session or session["user"] not in session_manager.users:
            return jsonify(did_succeed=False, message="Please register a username"), 401
        return f(*args, **kwargs)
    return decorated_function
