# tests/conftest.py
import pytest, time
from src import create_app, socketio
from src.models import UserModel, UserState, SessionState, SessionModel, db_session, session_votes
from flask import session


USER = 'test123'
ROOM = f'{USER}_room'


@pytest.fixture
def app():
    app_instance = create_app(debug=True)
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

def humanize_register(test_client):
    # Register the user
    response = test_client.post('/api/register', json={'username': USER})
    assert response.json['status'] == 'ok', "User register failed"

    return response.json

def humanize_host_room(room, test_client):
    response = test_client.post('/api/lobby', json={'type': 'host', 'room': room})
    assert response.json['content'] is not None, "Room host failed"

    return response.json

def humanize_join_ws_room(username, room, namespace=None, authenticated_ws_client=None):
    authenticated_ws_client.emit('join', {'room': room, 'username': username}, namespace=namespace)
    received = authenticated_ws_client.get_received('/chat')
    print(received)
    assert received[1]['args']['message'] == f"user 1/2 joined!"

    return received


def humanize_send_msg(username, room, msg, namespace, ws_client):
    msg_data = {
        'from': username,
        'room': room,
        'message': msg
    }
    ws_client.emit('message', msg_data, namespace=namespace)

    time.sleep(0.3)

    received = ws_client.get_received(namespace)
    assert received[0]['args']['message'] == 'Hello world!', "Message not sent correctly"
    assert received[0]['namespace'] == '/chat', "Namespace not correct"

    return received


def humanize_get_lobby_sessions(test_client):
    return test_client.get('/api/lobby/sessions').json


def humanize_ws_connect(ws_client, namespace=None):
    ws_client.connect(namespace)
    assert ws_client.is_connected(namespace)

def humanize_ws_connect_before_register(ws_client, namespace=None):
    humanize_ws_connect(ws_client=ws_client, namespace=namespace)
    ws_client.emit('join', {'room': ROOM, 'username': USER}, namespace='/chat')
    received = ws_client.get_received('/chat')[0]['args']
    assert received['message'] == 'User is not registered', 'Lingering session, why is there a session before register?'

    return received


def humanize_ws_disconnect(ws_client, namespace=None):
    ws_client.disconnect(namespace)
    assert not ws_client.is_connected(namespace)

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
        print("\nResponse received from register:")
        print(humanize_register(test_client=api_test_client))
        

        # Host a room
        print("\nResponse received from creating lobby: ")
        print(humanize_host_room(room=ROOM, test_client=api_test_client))

        # Get active,pending sessions
        print("\nResponse received from getting lobby sessions: ")
        print(humanize_get_lobby_sessions(test_client=api_test_client))


        # Connect to chat now that we have a room and user
        humanize_ws_connect(websockets_client, '/chat')

        # This test case tests the handling of a connection given the user's id. 
        # Using user's id to assert so it is consistent with the handle_connect() function. 
        with api_test_client.session_transaction() as sess:
            user_id = sess['user']

        with db_session() as db:
            tmp_user = db.query(UserModel).filter_by(id=user_id).one_or_none()
            assert tmp_user.state == UserState.ACTIVE, f"Expected ACTIVE, got {tmp_user.state}"
        
        # Disconnect from chat
        humanize_ws_disconnect(ws_client=websockets_client, namespace='/chat')

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
        print("\nResponse received from register:")
        print(humanize_register(test_client=api_test_client))

        # Host a room
        print("\nHosting room...\n")
        print(humanize_host_room(room=ROOM, test_client=api_test_client))


        # Connect to chat before registering user
        print("\nConnecting to ws before register...\n")
        print("\nResponse received from join before registering user: ")
        print(humanize_ws_connect_before_register(websockets_client, namespace='/chat'))

  
        # Connect to chat now that we have a room and user
        websockets_client_after_registering_user = socketio.test_client(app, flask_test_client=api_test_client)
        humanize_ws_connect(websockets_client_after_registering_user, '/chat')

        # Join the room
        print("\nJoining room...\n")
        print("\nResponse received from join after registering user: ")
        print(humanize_join_ws_room(username=USER, room=ROOM, namespace='/chat', authenticated_ws_client=websockets_client_after_registering_user))

        humanize_ws_disconnect(ws_client=websockets_client_after_registering_user, namespace='/chat')


    finally:
        print("\nCleaning up...")
        api_test_client.get('/api/logout')


# Test case 4
def test_handle_msg(app, websockets_client, api_test_client):
    try:
        # Register the user
        print("\nResponse received from register:")
        print(humanize_register(test_client=api_test_client))
        

        # Host a room
        print("\nResponse received from creating lobby: ")
        print(humanize_host_room(room=ROOM, test_client=api_test_client))
        

        # Connect to chat before registering user
        print("\nConnecting to ws before register...\n")
        print("\nResponse received from join before registering user: ")
        print(humanize_ws_connect_before_register(websockets_client, namespace='/chat'))


        # Connect to chat now that we have a room and user
        websockets_client_after_registering_user = socketio.test_client(app, flask_test_client=api_test_client)
        humanize_ws_connect(websockets_client_after_registering_user, '/chat')

        # Join the room
        print("\nJoining room...\n")
        print("\nResponse received from join after registering user: ")
        print(humanize_join_ws_room(username=USER, room=ROOM, namespace='/chat',authenticated_ws_client=websockets_client_after_registering_user))


        # Send message
        print("\nSending msg...")
        print("\nResponse received after sending msg: ")
        print(humanize_send_msg(username=USER, room=ROOM, msg='Hello world!', namespace='/chat', ws_client=websockets_client_after_registering_user))

        humanize_ws_disconnect(websockets_client_after_registering_user, '/chat')


    finally:
        print("\nCleaning up...")
        api_test_client.get('/api/logout')
