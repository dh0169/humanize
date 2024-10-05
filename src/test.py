import requests
import websocket
import json
import threading
import time
from queue import Queue

# Configuration
BASE_URL = "http://localhost:5000"  # Replace with your server's base URL
WS_URL = "ws://localhost:5000/chat"  # Replace with your WebSocket URL
NUM_USERS = 4

class User:
    def __init__(self, username):
        self.username = username
        self.session_cookie = None
        self.ws = None
        self.message_queue = Queue()

    def register(self):
        response = requests.post(f"{BASE_URL}/api/register", json={"username": self.username})
        if response.status_code == 200 and response.json()['did_succeed']:
            self.session_cookie = response.cookies.get_dict()
            return True
        return False

    def connect_ws(self):
        self.ws = websocket.WebSocketApp(
            WS_URL,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close,
            cookie=f"session={self.session_cookie['session']}"
        )
        threading.Thread(target=self.ws.run_forever).start()

    def on_message(self, ws, message):
        self.message_queue.put(json.loads(message))

    def on_error(self, ws, error):
        print(f"Error for {self.username}: {error}")

    def on_close(self, ws, close_status_code, close_msg):
        print(f"Closed connection for {self.username}")

def run_test():
    users = [User(f"user{i}") for i in range(NUM_USERS)]

    # Register users
    for user in users:
        assert user.register(), f"Failed to register {user.username}"
        print(f"Registered {user.username}")

    # Connect to WebSocket
    for user in users:
        user.connect_ws()
        print(f"Connected {user.username} to WebSocket")

    # Wait for initial connection messages
    time.sleep(2)

    # Simulate the session conversation
    expected_messages = [
        {"from": "Server", "message": "Game is starting..."},
        {"from": "Server", "message": "Some prompt here! Goodluck!"},
        {"from": "AI", "message": "Beep Boop 🤖"}
    ]

    for expected in expected_messages:
        for user in users:
            message = user.message_queue.get(timeout=30)  # Wait up to 30 seconds for each message
            assert message['from'] == expected['from'], f"Expected message from {expected['from']}, got {message['from']}"
            assert message['message'] == expected['message'], f"Expected message '{expected['message']}', got '{message['message']}'"
            print(f"{user.username} received: {message['from']}: {message['message']}")

    print("All expected messages received correctly.")

    # Close WebSocket connections
    for user in users:
        user.ws.close()

    print("Test completed successfully!")

if __name__ == "__main__":
    run_test()