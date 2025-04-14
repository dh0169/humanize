import pytest
from src import create_app, socketio


USER = 'testregisteruser7'
ROOM = f'{USER}_room'


@pytest.fixture
def app():
    app_instance = create_app()
    return app_instance

def test_api_root(app):
    test_client = app.test_client()
    response = test_client.get('/api/')
    print(response.json)

def test_user_and_room(app):
    test_client = app.test_client()
    response = test_client.post('/api/register', json={'username': USER})
    print(response.json)
    assert response.json['status'] == 'ok', "User register failed"

    response = test_client.post('/api/lobby', json={'type': 'host', 'room': ROOM})
    print(response.json)
    assert response.json['content'] is not None, "Room host failed"


    #Test websockets here

    websockets_client = socketio.test_client(app)
    websockets_client.emit('join', json={'room' : 'testhostsession', 'username' : 'testregisterus'})



    test_client.get('/api/logout')

   