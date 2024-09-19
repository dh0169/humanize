import string
import random


from functools import wraps
from flask import session, request, redirect
from flask_socketio import disconnect




def is_registered(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect('/')
        return f(*args, **kwargs)
    return decorated_function

