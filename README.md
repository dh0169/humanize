# Humanize - AI Among Us

**Humanize - AI Among Us** is a fun and engaging multiplayer game where 4-6 players are grouped in an online chat. The twist? One of the players is an AI! The goal of the human players is to work together, chat, and strategize to figure out which of them is actually an AI (a sneaky LLM). Can the humans fish out the AI before time runs out?

## Documentation Files

- **[README.md](README.md)**: This file provides an overview of the project, including its purpose, setup instructions, and basic usage guidelines. It serves as the primary introduction to the project for new users and contributors.

- **[API.md](API.md)**: This document details the API endpoints, request/response formats, and any authentication requirements for interacting with the chat server. It's essential for developers who want to integrate with or extend the chat functionality.

- **[DEBUG.md](DEBUG.md)**: This file contains instructions for using the Chat API Debug Page, a tool designed for testing and troubleshooting the chat functionality. It guides users through the process of registering, joining rooms, and sending messages for debugging purposes.


## Features

- **4-6 player online multiplayer game**
- **AI-powered**: One player is secretly an AI language model (LLM) trying to blend in with the humans.
- **Interactive gameplay**: Human players must use their communication skills to identify the AI.
- **Fun & suspense**: The game builds suspense as players chat and try to work out who is real and who is artificial.

## Tech Stack

- **Python 3.10+**: The game will be developed using Python. Python 3.10 is recommended for the most stable and modern experience.
- **LLM integration**: Using an AI language model to simulate one of the players.
- **Pip & Virtual Environments**: Dependency management and environment setup will be handled using `pip` and Python virtual environments (`venv`).

## Getting Started

### Prerequisites

- **Python 3.10+**: Make sure you have Python 3.10 or higher installed. You can download it [here](https://www.python.org/downloads/).
- **pip**: Ensure pip is installed for managing dependencies.
- **Virtualenv**: Create a virtual environment to keep dependencies organized.

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/humanize.git
    cd humanize
    ```

2. Create a virtual environment:
    ```bash
    python3 -m venv venv
    ```

3. Activate the virtual environment:

    On macOS/Linux:
    ```bash
    source venv/bin/activate
    ```

    On Windows:
    ```bash
    .\venv\Scripts\activate
    ```

4. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### Running the Game

```bash
python3 main.py
```


