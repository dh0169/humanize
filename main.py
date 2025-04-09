from src import create_app, socketio
from dotenv import load_dotenv, find_dotenv
import os

app = create_app(debug=False)

if __name__ == '__main__':

    env_path = find_dotenv()
    if not env_path:
        raise FileNotFoundError(".env file not found.")
        
    load_dotenv(env_path)

    HOST = "0.0.0.0"
    PORT = 8080

    socketio.run(app, host=HOST, port=int(PORT), debug=False, log_output=True)