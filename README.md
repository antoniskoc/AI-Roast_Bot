# Ai Roast Bot

A Python bot that listens to messages in a Messenger group and generates AI-powered replies using Groq.

This project was built purely for fun, It utilizes a facebook account to act as the bot's identity in Messenger group chats.
It is currently set up so that is makes fun of one of my best friends for moving to the capital (its an inside joke). But can easily be set up to make fun of anything you want.

Instead of logging in with a username and password, the application uses an authenticated Facebook session stored in a local JSON file.

## Features

- **Automatic replies** Watches one configured messenger group and listens for a message from one user, as things are it replies to every message sent by that user( with a 30 second cooldown).
- **Ai generated personalised roasts** Sends the message to a model of Groq, then generates a short reply in polish.
- **Message filtering:** Ignores other chats and other users.
- **Configuration through environment variables:** Keeps the API key and target IDs out of the source code


## Tech used

- **Python** - bot logic and asynchronous message handling
- **[fbchat-mugit](https://pypi.org/project/fbchat-muqit/)** - the unofficial Messenger client, very easy to use and quite versitile. 
- **[Groq API](https://console.groq.com/)** - AI text generation
- **OpenAI Python SDK** - asynchronous API client (`AsyncOpenAI`)
-**python-dotenv** - local enviroment configuration

## How is all works

1. the program starts the Messenger client.
2. The client listens for incoming Messenger events.
3. If the message sender ID and group ID match and the cooldown is over, it sents the message to the AI generator.
4. The generated response is sent back to the same group chat using the bot account.

The cooldown and *currently generating* flag are kept in memory. They reset when the program restarts.

## Project structure

```text
AI-Roast_Bot/
├── main.py                # Starts the Messenger bot
├── messenger_listener.py  # Message handling, filtering and cooldown
├── ai_generator.py        # Groq API integration and standalone generator check
├── requirements.txt       # Python dependencies
├── .env.example           # Example environment configuration
├── .gitignore
└── cookies/
    └── session.json       # Local Messenger session
```

the `cookies/` dir and `.env` file are excluded from Git on purpose. These are for you to fill with your messenger session data, groq API, Group target ID, and target user id.

## How to use

### 1. Download the code

Clone or download this repository, then open the project folder in a terminal

### 2. Create a virtual enviroment and install dependencies
For Windows:
```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```
For Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

### 3. Configure Groq

Copy the contents of `.env.example` to a new file named `.env`, then fill out with your own values


- `GROQ_API_KEY` — your Groq API key.
- `TARGET_THREAD_ID` — the ID of the Messenger group to monitor.
- `TARGET_USER_ID` — the ID of the group participant the bot should respond to.

**How to get your Groq API key**
1. Sign in to the [Groq Console](https://console.groq.com/keys).
2. Select a project if the console asks you to, then choose **Create APi key*
3. Copy the generated key and paste it accordingly

**How to Connect a Messenger account and find target IDs**

The bot acts through an existing Facebook account. I reccomend using a dedicated account rather than a personal account.

The project does **not** create a new Facebook account or perform an interactive login. Instead, `fbchat-muqit` loads an already authenticated session from a local JSON file:

```python
client = Client(cookies_file_path="cookies/session.json")
```

1. Obtain a valid session file for the bot account.( press F12 on chrome , open the Applications tab, copy the **c_user** and **xs** values)
2. Paste these values to a file like this 
```json
[
  {
    "name": "c_user",
    "value": "YOUR_C_USER_COOKIE_VALUE"
  },
  {
    "name": "xs",
    "value": "YOUR_XS_COOKIE_VALUE"
  }
]
```
3. Save it locally under `cookies/session.json`
4. Add the bot account to your messenger group
5. Start the listener with `python main.py`
6. Wait for the roast victim to sent a text message in the group, and then look at the terminal output. You should see something similar to:
```text
   Group ID: <group-id>
   Sender ID: <user-id>
   ```
7. Copy the **Group ID** into `TARGET_THREAD_ID` and the **Sender ID** to `TARGET_USER_ID`.
8. Stop the bot by pressing **Ctrl+C**, save `.env`, then restart is with `python main.py`

9. Enjoy unlimited roasts

### Additional AI generator test

to check Groq generation without starting the Messenger listener, run:

```bash
python ai_generator.py
```

This runs a small built-in example using the message `Dzisiaj znowu gram w LoLa` and prints the generated roast. **It makes a real API request.**


### Limitations and future 

- The program so far onlu supports one target group and one user, i hope to expand the number of groups and users.
- The Messenger integration uses an unofficial library and could break following changes to Facebook/Messenger or run into account/platform restrictions.

--- 
This project is deliberately silly and customized for my needs primarily, to edit the ai prompt simply go to `ai_generator.py` and edit the Groq prompt however you see fit.