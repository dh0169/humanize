# Chat API Documentation

Base URL: `http://localhost:5000/api`

## Endpoints

### 1. Index

Get the API status.

- **URL:** `/`
- **Method:** `GET`
- **Response:**
  - **Code:** 200 OK
  - **Content:** 
    ```json
    {
      "message": "Chat API is running"
    }
    ```

### 2. Register

Register a new user.

- **URL:** `/register`
- **Method:** `POST`
- **Data Params:** 
  ```json
  {
    "username": "[string]"
  }
  ```
- **Success Response:**
  - **Code:** 200 OK
  - **Content:** 
    ```json
    {
      "did_succeed": true,
      "message": "Registration Success!",
      "data": {
        "user": "[username]"
      }
    }
    ```
- **Error Response:**
  - **Code:** 200 OK
  - **Content:** 
    ```json
    {
      "did_succeed": false,
      "message": "User already exists"
    }
    ```

### 3. Lobby

Get user information or perform lobby actions.

- **URL:** `/lobby`
- **Method:** `GET`
- **Success Response:**
  - **Code:** 200 OK
  - **Content:** 
    ```json
    {
      "message": "Welcome [username]!",
      "data": {
        "user": {
          // User object
        }
      }
    }
    ```

- **Method:** `POST`
- **Data Params:**
  ```json
  {
    "type": "join",
    "room": "[string]",
    "random": "[boolean]"
  }
  ```
  or
  ```json
  {
    "type": "host",
    "room": "[string]"
  }
  ```
- **Success Response:**
  - **Code:** 200 OK
  - **Content:** 
    ```json
    {
      "message": "[Success message]",
      "data": {
        "room": "[room name]"
      },
      "did_succeed": true,
      "socketio": "http://localhost:5000/chat"
    }
    ```
- **Error Response:**
  - **Code:** 200 OK
  - **Content:** 
    ```json
    {
      "message": "[Error message]",
      "data": {
        "room": "[room name]"
      },
      "did_succeed": false
    }
    ```

### 4. List Lobby Sessions

Get a list of pending and active sessions.

- **URL:** `/lobby/sessions`
- **Method:** `GET`
- **Success Response:**
  - **Code:** 200 OK
  - **Content:** 
    ```json
    {
      "message": "Sessions available to join",
      "pending_sessions": [
        // Array of session objects
      ],
      "active_sessions": [
        // Array of session objects
      ]
    }
    ```

### 5. List Users

Get a list of all users.

- **URL:** `/lobby/users`
- **Method:** `GET`
- **Success Response:**
  - **Code:** 200 OK
  - **Content:** 
    ```json
    {
      "message": "Users in game",
      "users": [
        // Array of user objects
      ]
    }
    ```

### 6. Logout

Logout the current user.

- **URL:** `/logout`
- **Method:** `GET`
- **Success Response:**
  - **Code:** 200 OK
  - **Content:** 
    ```json
    {
      "message": "Logout successful. Adios, pal."
    }
    ```
- **Error Response:**
  - **Code:** 200 OK
  - **Content:** 
    ```json
    {
      "message": "No session found"
    }
    ```

## Notes

- All endpoints except `/register` and `/` require user authentication.
- Authentication is handled through session cookies.
- The maximum username length is 30 characters.
- When joining a room, you can either specify a room name or set `random` to true to join a random room.
- The API returns HTTP status 401 if a user tries to access a protected endpoint without being registered.
