# Chat API Documentation

## Overview

This API provides functionality for a real-time chat application, including user registration, session management, and messaging. It uses SQLAlchemy for database interactions, Flask for the RESTful API endpoints, and Flask-SocketIO for real-time communication.

## Base URL

All REST endpoints are prefixed with `/api`.
All WebSocket events use the namespace `/chat`.

## Models

### UserModel

Represents a user in the system.

- `id`: Integer, primary key
- `username`: String(30), not null
- `session_id`: Integer, foreign key to SessionModel
- `state`: Enum(UserState), default WAITING

### SessionModel

Represents a chat session.

- `id`: Integer, primary key
- `room`: String(100), unique
- `robot`: String(20), nullable (AI Model Name)
- `host_id`: Integer, foreign key to UserModel
- `state`: Enum(SessionState), default PENDING
- `max_players_allowed`: Integer, default 4

### MessageModel

Represents a message in a chat session.

- `id`: Integer, primary key
- `sender`: String, foreign key to UserModel.username
- `session_id`: Integer, foreign key to SessionModel
- `message`: String, not null
- `timestamp`: DateTime, not null

## REST Endpoints

### GET /api/

Check if the API is running.

**Response:**
- Status: 200 OK
- Body: `{"message": "Chat API is running"}`

### GET /api/lobby

Get information about the current user.

**Authentication Required**

**Response:**
- Status: 200 OK
- Body: `{"message": "Welcome {username}!", "data": {"user": {...}}}`

### POST /api/lobby

Join or host a chat session.

**Authentication Required**

**Request Body:**
```json
{
  "type": "join" | "host",
  "room": "room_name",
  "random": true | false  // Only for join type
}
```

**Response:**
- Status: 200 OK
- Body: 
  ```json
  {
    "message": "...",
    "data": {"room": "room_name"},
    "did_succeed": true | false,
    "ws": "websocket_url"
  }
  ```

### GET /api/lobby/sessions

List all pending and active game sessions.

**Response:**
- Status: 200 OK
- Body:
  ```json
  {
    "message": "Game sessions",
    "pending_sessions": [...],
    "active_sessions": [...]
  }
  ```

### GET /api/lobby/users

List all registered users.

**Response:**
- Status: 200 OK
- Body:
  ```json
  {
    "message": "Registered users",
    "users": [...]
  }
  ```

### POST /api/register

Register a new user.

**Request Body:**
```json
{
  "username": "user_name"
}
```

**Response:**
- Status: 200 OK
- Body:
  ```json
  {
    "did_succeed": true | false,
    "message": "...",
    "data": {"user": "username"}
  }
  ```

### GET /api/logout

Logout the current user.

**Authentication Required**

**Response:**
- Status: 200 OK
- Body: `{"message": "Logout successful. Adios, pal."}`

## WebSocket Events

### connect

Triggered when a client connects to the WebSocket.

**Authentication Required**

### disconnect

Triggered when a client disconnects from the WebSocket.

**Authentication Required**

### join

Join a chat room.

**Authentication Required**

**Emit:**
```json
{
  "room": "room_name",
  "username": "user_name"
}
```

**Receive:**
- Success: Server message in the room
- Error: `{'msg': 'Username and room name are required!'}`

### message

Send a message in a chat room.

**Authentication Required**

**Emit:**
```json
{
  "from": "sender_username",
  "room": "room_name",
  "message": "message_content"
}
```

**Receive:**
- Success: Message broadcasted to the room
- Error: No response (message not sent)

## Authentication

The API uses session-based authentication. After successful registration, the user's ID is stored in the session.

## Error Handling

The API uses the `@handle_db_errors` decorator to catch and handle database-related errors. Specific error responses are not detailed in this documentation but should be handled appropriately in the client application.

## WebSocket Integration

The API provides WebSocket functionality for real-time communication. The WebSocket URL is returned in the response when joining or hosting a session via the REST API.

## Usage Notes

1. Users must register and join a session before they can send messages.
2. The `session_manager` handles user connections, disconnections, and session management.
3. Messages are stored in the database and associated with their respective sessions.
4. The API supports an AI bot feature, indicated by the `robot` field in the `SessionModel`.

## Best Practices

1. Always authenticate before attempting to join a room or send messages.
2. Handle WebSocket disconnections gracefully on the client-side and attempt to reconnect.
3. Implement proper error handling for both REST API calls and WebSocket events.
4. Use the provided `to_dict()` methods when working with model instances to ensure consistent data representation.