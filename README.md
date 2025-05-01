# FOMO Bot

A Discord bot that monitors whitelisted messages in channels and provides summarization features.

## Features

- Scans pinned messages for "FomoBot Whitelist" to identify whitelisted channels and users
- Tracks messages from whitelisted users in selected channels
- Provides message history command (`!history`) to display recent messages
- Offers summarization command (`!summarize`) to create concise summaries of conversations
- Integration with Google Vertex AI (Gemini) for message summarization

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

4. Create a `.env` file in the project root with the following settings:
```
DISCORD_TOKEN=your_discord_bot_token
GOOGLE_GCP_REGION=your_gcp_region
GOOGLE_GCP_PROJECT_ID=your_google_cloud_project_id
```

5. Run the bot:
```bash
poetry run python main.py
```

## Usage

### Setting Up a Whitelist

1. Create a pinned message in a channel with the content "FomoBot Whitelist"
2. React to this message with a ✅ emoji
3. Any users who add a ✅ reaction to this message will be whitelisted

### Bot Commands

- `!history` - Displays the recent messages from whitelisted users in an embed format (limited to 25 messages)
- `!summarize` - Generates a concise summary of the conversation using Google Vertex AI

## Google Vertex AI Integration

The bot uses Google's Vertex AI API with Gemini models for text summarization. Key features:

- Uses the `gemini-2.0-flash-001` model for efficient processing
- Structures message data for optimal summarization
- Maintains message context and conversation flow in summaries

## Bot Permissions

The bot needs the following permissions:
- Read Messages/View Channels
- Send Messages
- Read Message History
- Manage Messages (for reading pinned messages)
- Add Reactions (for processing whitelist reactions)

## Development Notes

The project uses:
- Python 3.13
- discord.py 2.3.2
- Kink dependency injection
- Google Cloud AI Platform
- Poetry for dependency management

## Setting Up a Discord Bot

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a new application
3. Navigate to the "Bot" tab
4. Click "Add Bot"
5. Copy the token and add it to your `.env` file
6. Under "Privileged Gateway Intents", enable "Message Content Intent"
7. Use the OAuth2 URL Generator to create an invite link with appropriate permissions 