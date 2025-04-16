# tests/conftest.py
import pytest, time
from src import create_app, socketio
from src.models import UserModel, UserState, SessionState, SessionModel, db_session, session_votes
from flask import session


USER = 'test123'
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

# Test case 1 & 2
def test_handle_connect_disconnect(websockets_client, api_test_client):    
    try:
        # Connect to chat
        websockets_client.connect('/chat')
        resp = websockets_client.get_received('/chat')[0]['args']
        print("\nResponse received from connect: ")
        print(resp)
        # This line tests the handling of a non-registered user connecting to the websockets.
        assert resp['message'] == 'User is not registered', "Lingering session, why is there a session before register?"
        websockets_client.disconnect('/chat')
        assert not websockets_client.is_connected('/chat')

        # Register the user
        print("\nResponse received from register: ")
        response = api_test_client.post('/api/register', json={'username': USER})
        print(response.json)
        assert response.json['status'] == 'ok', "User register failed"

        # Host a room
        response = api_test_client.post('/api/lobby', json={'type': 'host', 'room': ROOM})
        print("\nResponse received from creating lobby: ")
        print(response.json)
        assert response.json['content'] is not None, "Room host failed"

        print("\nResponse received from getting lobby sessions: ")
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
        
        # Disconnect from chat
        websockets_client.disconnect('/chat')
        assert not websockets_client.is_connected('/chat')

        # This test case tests the handling of a disconnection given the user's id.
        with db_session() as db:
            tmp_user = db.query(UserModel).filter_by(id=user_id).one_or_none()
            assert tmp_user.state == UserState.DISCONNECTED, f"Expected ACTIVE, got {tmp_user.state}"

    finally:
        print("\nCleaning up...")
        api_test_client.get('/api/logout')

# Test case 3
def test_handle_join(app, websockets_client, api_test_client):
    try:
        # Register the user
        response = api_test_client.post('/api/register', json={'username': USER})
        print(response.json)
        assert response.json['status'] == 'ok', "User register failed"

        # Host a room
        response = api_test_client.post('/api/lobby', json={'type': 'host', 'room': ROOM})
        print("\nHosting room...\n")
        print(response.json)
        assert response.json['content'] is not None, "Room host failed"

        # Connect to chat before registering user
        websockets_client.connect('/chat')
        assert websockets_client.is_connected('/chat')
        websockets_client.emit('join', {'room': ROOM, 'username': USER}, namespace='/chat')
        received = websockets_client.get_received('/chat')[0]['args']
        print("\nResponse received from join before registering user: ")
        print(received)
        assert received['message'] == 'User is not registered', 'Lingering session, why is there a session before register?'

  
        # Connect to chat now that we have a room and user
        websockets_client_after_registering_user = socketio.test_client(app, flask_test_client=api_test_client)
        websockets_client_after_registering_user.connect('/chat')
        assert websockets_client_after_registering_user.is_connected('/chat')

        # Join the room
        print("\nJoining room...\n")
        websockets_client_after_registering_user.emit('join', {'room': ROOM, 'username': USER}, namespace='/chat')
        received = websockets_client_after_registering_user.get_received('/chat')[0]['args']
        print("\nResponse received from join after registering user: ")
        print(received)
        assert received['message'] == f"<User(id=1, username='{USER}', session_id=1, state=UserState.ACTIVE)> has connected to /chat"

        websockets_client_after_registering_user.disconnect('/chat')


    finally:
        print("\nCleaning up...")
        api_test_client.get('/api/logout')


# Test case 4
def test_handle_msg(app, websockets_client, api_test_client):
    try:
        # Register the user
        response = api_test_client.post('/api/register', json={'username': USER})
        print(response.json)
        assert response.json['status'] == 'ok', "User register failed"

        # Host a room
        response = api_test_client.post('/api/lobby', json={'type': 'host', 'room': ROOM})
        print("\nHosting room...\n")
        print(response.json)
        assert response.json['content'] is not None, "Room host failed"

        # Connect to chat before registering user
        websockets_client.connect('/chat')
        assert websockets_client.is_connected('/chat')
        websockets_client.emit('join', {'room': ROOM, 'username': USER}, namespace='/chat')
        received = websockets_client.get_received('/chat')[0]['args']
        print("\nResponse received from join before registering user: ")
        print(received)
        assert received['message'] == 'User is not registered', 'Lingering session, why is there a session before register?'
        # Connect to chat now that we have a room and user
        websockets_client_after_registering_user = socketio.test_client(app, flask_test_client=api_test_client)
        websockets_client_after_registering_user.connect('/chat')
        assert websockets_client_after_registering_user.is_connected('/chat')

        # Join the room
        print("\nJoining room...\n")
        websockets_client_after_registering_user.emit('join', {'room': ROOM, 'username': USER}, namespace='/chat')
        received = websockets_client_after_registering_user.get_received('/chat')[0]['args']
        print("\nResponse received from join after registering user: ")
        print(received)
        assert received['message'] == f"<User(id=1, username='{USER}', session_id=1, state=UserState.ACTIVE)> has connected to /chat"

        msg_data = {
            'from': USER,
            'room': ROOM,
            'message': 'Hello world!'
        }
        websockets_client_after_registering_user.emit('message', msg_data, namespace='/chat')
        received = websockets_client_after_registering_user.get_received('/chat')
        print("\nResponse received after sending message: ")
        print(received)
        assert received[0]['args']['message'] == 'Hello world!', "Message not sent correctly"
        assert received[0]['namespace'] == '/chat', "Namespace not correct"


        websockets_client_after_registering_user.disconnect('/chat')


    finally:
        print("\nCleaning up...")
        api_test_client.get('/api/logout')
