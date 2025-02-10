# Discord Bot for Tracking Status and Most Recent Message

This bot tracks the user's current status and the most recent message sent by them.

---

## Prerequisites

1. A Discord bot token (API key).
2. Python installed on your local machine.
3. The `discord.py` and `pandas` libraries installed.

---

## Setup Instructions

### 1. Create a Discord Bot

To use the bot, you first need to create a Discord bot and get the API key.

1. Visit the [Discord Developer Portal](https://discord.com/developers/applications).
2. Create a new application by clicking on **"New Application"**.
3. In your application, go to the **"Bot"** section and click **"Add Bot"**.
4. Under the bot section, copy the **Token**. This is your `API_KEY`.

---

### 2. Create the Config File

Once you have your `API_KEY`, create a file named `config.py` and insert the following:

```python
api_key = "YOUR_API_KEY_HERE"

# Logging setup
import logging

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

```

### 3. Run code
```bash
py bot.py
```
