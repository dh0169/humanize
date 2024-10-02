from src import create_app, socketio
from dotenv import load_dotenv, find_dotenv

app = create_app(debug=True)

if __name__ == '__main__':
    load_dotenv()

    env_path = find_dotenv()
    if not env_path:
        raise FileNotFoundError(".env file not found.")

    socketio.run(app, host="0.0.0.0")

