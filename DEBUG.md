# Chat API Debug Page Instructions
This document provides instructions on how to use the Chat API Debug Page to test and troubleshoot the chat functionality.

## Getting Started

Open the HTML file in a web browser. You should see a page titled "Chat API Debug Page" with several sections.
Ensure that your Chat API server is running on http://localhost:5000. If your server is running on a different address, update the API_URL constant in the JavaScript code in "templates/debug.html"

![image](/imgs/debug.png)


## Using the Debug Page

### 1. Register a User

- In the "Register" section, enter a username in the input field.
- Click the "Register" button.
- If successful, you'll see a message confirming your registration.

### 2. Join or Host a Room

- In the "Join or Host a Room" section, enter a room name in the input field.
- To join an existing room, click "Join Room".
- To create and host a new room, click "Host Room".
- To join a random available room, click "Join Random Room".
- Upon successful connection, the chat section will appear.

### 3. View Lobby Information

- Click "List Lobby Sessions" to see pending and active chat sessions.
- Click "List Lobby Users" to see users currently in the lobby.

### 4. Chat

- Once connected to a room, the chat section will appear at the bottom of the page.
- Type your message in the input field and click "Send" or press Enter to send a message.
- Sent and received messages will appear in the chat window above the input field.

### 5. Logout

- To logout and disconnect from the chat, click the "Logout" button in the Register section.
