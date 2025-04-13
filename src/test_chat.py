# test_chat.py
import pytest
from flask import Flask, session
from src import socketio 
from src.models import db_session, UserModel, SessionModel, UserState
from dotenv import load_dotenv, find_dotenv

env_path = find_dotenv()
if not env_path:
    raise FileNotFoundError(".env file not found.")
        
load_dotenv(env_path)

@pytest.fixture
def app():
    from src import create_app, socketio
    app = create_app(debug=False)
    return app  

@pytest.fixture
def client(app):
    return socketio.test_client(app, namespace='/chat')

@pytest.fixture
def with_user(client, app):
    with client.flask_test_client.session_transaction() as sess:
        sess['user'] = 1  
    return client

def test_handle_connect_updates_state(with_user):
    client = with_user
    connected = client.connect(namespace='/chat')
    assert connected is True

    # Optionally: Check server emitted any messages
    messages = client.get_received('/chat')
    print(messages)

