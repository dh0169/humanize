from src import create_app, socketio
from dotenv import load_dotenv, find_dotenv
import os

app = create_app(debug=True)

if __name__ == '__main__':

    env_path = find_dotenv()
    if not env_path:
        raise FileNotFoundError(".env file not found.")
        
    load_dotenv(env_path)

    HOST = os.environ.get("HUMANIZE_HOST")
    PORT = os.environ.get("HUMANIZE_PORT")

    if not HOST:
        HOST = "127.0.0.1"

    if not PORT:
        PORT = 5000

    socketio.run(app, host=HOST, port=int(PORT))