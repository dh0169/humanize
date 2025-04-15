# tests/conftest.py
import pytest, time
from src import create_app, socketio
from src.models import UserModel, UserState, SessionState, SessionModel, db_session, session_votes
from flask import session


USER = 'testregisteruser7'
ROOM = f'{USER}_room'


@pytest.fixture
def app():
    app_instance = create_app()
    return app_instance
    
@pytest.fixture
def api_test_client(app):
    client = app.test_client()
    response = client.get('/api/')
    assert response.json['status'] == 'ok'
    return client

@pytest.fixture
def websockets_client(app, api_test_client):
    ws_client = socketio.test_client(app, flask_test_client=api_test_client)
    ws_client.connect('/chat')
    assert ws_client.is_connected('/chat')
    return ws_client

def test_handle_connect(websockets_client, api_test_client):    
    try:
        # Connect to chat
        websockets_client.connect('/chat')
        resp = websockets_client.get_received('/chat')[0]['args']
        print(resp)
        # This line tests the handling of a non-registered user connecting to the websockets.
        assert resp['message'] == 'User is not registered', "Lingering session, why is there a session before register?"

        # Register the user
        response = api_test_client.post('/api/register', json={'username': USER})
        print(response.json)
        assert response.json['status'] == 'ok', "User register failed"

        # Host a room
        response = api_test_client.post('/api/lobby', json={'type': 'host', 'room': ROOM})
        print(response.json)
        assert response.json['content'] is not None, "Room host failed"

        print(api_test_client.get('/api/lobby/sessions').json)

        # Connect to chat now that we have a room and user
        websockets_client.connect('/chat')
        assert websockets_client.is_connected('/chat')

        # This test case tests the handling of a connection given the user's id. 
        # Using user's id to assert so it is consistent with the handle_connect() function. 
        with api_test_client.session_transaction() as sess:
            user_id = sess['user']

        with db_session() as db:
            tmp_user = db.query(UserModel).filter_by(id=user_id).one_or_none()
            assert tmp_user.state == UserState.ACTIVE, f"Expected ACTIVE, got {tmp_user.state}"
        

        # Test joining a room
        #websockets_client.emit('join', json={'room': ROOM, 'username': USER})
        #print(websockets_client.get_received('/chat'))

    finally:
        print("\nCleaning up...")
        websockets_client.disconnect('/chat')
        api_test_client.get('/api/logout')

   