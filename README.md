# Humanize - AI Among Us

**Humanize - AI Among Us** is a fun and engaging multiplayer game where 4-6 players are grouped in an online chat. The twist? One of the players is an AI! The goal of the human players is to work together, chat, and strategize to figure out which of them is actually an AI (a sneaky LLM). Can the humans fish out the AI before time runs out?

## Features

- **4-6 player online multiplayer game**
- **AI-powered**: One player is secretly an AI language model (LLM) trying to blend in with the humans.
- **Interactive gameplay**: Human players must use their communication skills to identify the AI.
- **Fun & suspense**: The game builds suspense as players chat and try to work out who is real and who is artificial.


## Getting Started

### Prerequisites

- **Python 3.10+**: Make sure you have Python 3.10 or higher installed. You can download it [here](https://www.python.org/downloads/).
- **pip**: Ensure pip is installed for managing dependencies.
- **Virtualenv**: Create a virtual environment to keep dependencies organized.
- **.env file**: Create a .env file with the following variables defined(Note:This is an expensive app to run for gpt, api keys beware):

SECRET_KEY="secureflaskkey"
OPENAI_API_KEY="openai api key" 
DATABASE_URI="sqlite:///humanize.db"
FLASK_USER="debug username here"
FLASK_PW="debug password here"
HUMANIZE_HOST="ip addr here"
HUMANIZE_PORT="port number"


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

This will 
```bash
python3 main.py
```


