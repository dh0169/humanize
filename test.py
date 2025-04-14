# tests/conftest.py
import pytest, time
from src import create_app, socketio


USER = 'testregisteruser7'
ROOM = f'{USER}_room'


@pytest.fixture
def app():
    app_instance = create_app()
    return app_instance

# @pytest.fixture
# def websockets_client(app):
#     # Using Flask-SocketIO's test_client which creates a simulated connection
#     test_client = socketio.test_client(app)
#     yield test_client ## tes
#     # Disconnect the test client after tests
#     test_client.disconnect()

def test_baseline(app):
    api_test_client = app.test_client()
    response = api_test_client.get('/api/')
    print(response.json)
    assert response.json['status'] == 'ok', "Failed to get api root route."
    
    websockets_client = socketio.test_client(app)
    websockets_client.connect('/chat')
    print(websockets_client.get_received('/chat'))

    

    

    


def test_user_and_room(app):
    # Create a Flask test client that uses cookies
    api_test_client = app.test_client()
    
    try:

        #Create websocket        
        websockets_client = socketio.test_client(app=app, flask_test_client=api_test_client) # This creates a websocket test client with the cookie that is in the api test_client
        
        # Connect to chat
        websockets_client.connect('/chat')
        resp = websockets_client.get_received('/chat')[0]['args']
        print(resp)
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


        # Connect to chat
        websockets_client.connect('/chat')
        resp = websockets_client.get_received('/chat')
        assert not resp, "Failed to connect to /chat, is there a cookie?"


        # Test joining a room
        websockets_client.emit('join', json={'room': ROOM, 'username': USER})
        print(websockets_client.get_received('/chat'))

    finally:
        api_test_client.get('/api/logout')

   