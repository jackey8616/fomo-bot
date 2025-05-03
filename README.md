# FOMO Bot

A Discord bot that monitors whitelisted messages in channels and provides summarization features.

## Features

- Multiple user tracking strategies:
  - Role-based tracking: Tracks users with the "FomoTrack" role across the guild
  - Pinned message tracking: Scans pinned messages for "FomoBot TrackList" keyword and tracks users who react with ✅
- Provides two summarization modes:
  - Casual summarization (`/casual_summarize`) - Quick, concise summary of recent messages
  - Serious summarization (`/serious_summarize`) - Detailed, structured summary with message links
- Integration with Google Vertex AI (Gemini) for message summarization
- Flexible architecture with dependency injection using Kink
- Timezone conversion to Asia/Taipei (UTC+8) for all timestamps

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
poetry run python src/main.py
```

## Docker Support

You can also run the bot using Docker:

```bash
docker build -t fomo-bot .
docker run -d --env-file .env fomo-bot
```

## Usage

### Setting Up User Tracking

#### Role-Based Tracking
The bot automatically tracks users with the "FomoTrack" role. Users with this role will be monitored in all channels.

#### Pinned Message Tracking
1. Create a pinned message in a channel with the content containing "FomoBot TrackList"
2. React to this message with a ✅ emoji
3. Any users who add a ✅ reaction to this message will be tracked in that channel

### Bot Commands

- `/casual_summarize [channel]` - Generates a concise summary of the conversation in a casual format. Optionally specify a channel to summarize.
- `/serious_summarize [channel]` - Generates a detailed, structured summary of the conversation with timestamps and links to original messages. Optionally specify a channel to summarize.

## Google Vertex AI Integration

The bot uses Google's Vertex AI API with Gemini models for text summarization. Key features:

- Uses the `gemini-2.0-flash-001` model for efficient processing
- Implements different summarization strategies for different use cases
- Maintains message context and conversation flow in summaries
- Converts message timestamps to Asia/Taipei timezone (UTC+8)
- Includes links to original messages in serious summaries

## Bot Permissions

The bot needs the following permissions:
- Read Messages/View Channels
- Send Messages
- Read Message History
- Manage Messages (for reading pinned messages)
- Add Reactions (for processing whitelist reactions)
- View Members (for role-based tracking)
- Use Application Commands (for slash commands)

## Project Architecture

The project uses:
- Python 3.13
- discord.py 2.3.2
- Kink for dependency injection
- Google Cloud Vertex AI
- Poetry for dependency management

### Key Components

- `main.py` - Entry point that initializes and runs the bot
- `bootstrap.py` - Environment configuration and dependency injection setup
- `bot_client.py` - Main Discord bot implementation with command handling
- `user_tracking/` - Strategies for tracking users in channels
  - `user_tracking_strategy.py` - Base strategy interface
  - `pinned_message_emoji_tracker.py` - Tracks users via pinned message reactions
  - `role_based_tracker.py` - Tracks users based on their roles
  - `user_tracking_manager.py` - Manages multiple tracking strategies
- `summarize.py` - Provides different summarization strategies
- `google_vertex.py` - Integration with Google Vertex AI

## Setting Up a Discord Bot

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a new application
3. Navigate to the "Bot" tab
4. Click "Add Bot"
5. Copy the token and add it to your `.env` file
6. Under "Privileged Gateway Intents", enable:
   - Message Content Intent
   - Server Members Intent
   - Presence Intent
7. Navigate to the "OAuth2" tab
8. Select "bot" and "applications.commands" scopes
9. Select the required permissions from the "Bot Permissions" section
10. Use the generated URL to invite the bot to your server 