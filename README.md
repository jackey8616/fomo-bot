# FOMO Bot

A Discord bot that scans pinned messages across all text channels for the "FOMO" keyword.

## Features

- Automatically scans all pinned messages every hour
- Sends an alert when a pinned message containing "FOMO" is found
- Manual scan command available
- Case-insensitive keyword detection

## Setup

1. Install Poetry if you haven't already:
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

2. Clone this repository and navigate to its directory

3. Install dependencies using Poetry:
```bash
poetry install
```

4. Create a `.env` file in the project root and add your Discord bot token:
```
DISCORD_TOKEN=your_bot_token_here
```

5. Run the bot:
```bash
poetry run python bot.py
```

## Usage

- The bot will automatically scan pinned messages every hour
- Use the `!scan` command to manually trigger a scan
- When a FOMO keyword is found, the bot will send an alert with:
  - The channel where it was found
  - A link to the message
  - The message content

## Bot Permissions

The bot needs the following permissions:
- Read Messages/View Channels
- Send Messages
- Read Message History
- Manage Messages (for reading pinned messages)

## Note

Make sure to invite the bot to your server with the proper permissions enabled. 