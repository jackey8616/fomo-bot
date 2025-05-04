# FOMO Bot

A Discord bot that monitors and tracks users's messages in channels and provides summarization features with multi-language support.

## Features

- Multiple user tracking strategies:
  - Role-based tracking: Tracks users with the "FomoTrack" role across channels
  - Pinned message tracking: Scans pinned messages for "FomoBot TrackList" keyword and tracks users who react with ✅
  - Extensible tracking architecture through the `UserTrackingStrategy` interface and `UserTrackingManager`
- Two summarization modes:
  - Casual summarization (`/casual_summarize`) - Quick, concise summary of recent messages
  - Serious summarization (`/serious_summarize`) - Detailed, structured summary with message links
- Google Vertex AI integration using Gemini 2.0 Flash model for intelligent message summarization
- Multi-language support (English and Traditional Chinese) for commands and responses
- Dependency injection architecture using Kink for flexible component management
- Timezone conversion to Asia/Taipei (UTC+8) for consistent timestamp display

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
The bot automatically tracks users with the "FomoTrack" role. Create this role in your Discord server and assign it to users whose messages you want to track.

#### Pinned Message Tracking
1. Create a message containing the phrase "FomoBot TrackList" in the channel you want to monitor
2. Pin this message to the channel
3. Users can add a ✅ reaction to this pinned message to be tracked in that channel

### Bot Commands

- `/casual_summarize [channel]` - Generates a concise summary of tracked users' messages in a casual format. Optionally specify a channel to summarize.
- `/serious_summarize [channel]` - Generates a detailed, structured summary with timestamps and links to original messages. Optionally specify a channel to summarize.

Both commands support English and Traditional Chinese localization.

## Google Vertex AI Integration

The bot uses Google's Vertex AI with Gemini models for intelligent text summarization:

- Uses the `gemini-2.0-flash-001` model for efficient processing
- Implements different prompt strategies for casual vs. serious summarization needs
- Maintains message context and conversation flow in summaries
- Converts message timestamps to Asia/Taipei timezone (UTC+8)
- Includes jump links to original messages in serious summaries

## Bot Permissions

The bot requires the following Discord permissions:
- Read Messages/View Channels
- Send Messages
- Read Message History
- Manage Messages (for accessing pinned messages)
- Add Reactions (for reaction processing)
- View Guild Members (for role-based tracking)
- Use Application Commands (for slash commands)

## Project Architecture

The project uses:
- Python 3.13
- discord.py 2.3.2
- Kink for dependency injection
- Google Cloud Vertex AI for AI summarization
- pytz for timezone handling
- Poetry for dependency management

### Key Components

- `main.py` - Entry point that initializes the bot
- `bootstrap.py` - Environment configuration and dependency injection setup
- `bot_client.py` - Main Discord bot implementation with command handlers
- `translator.py` - Multi-language support for bot commands and responses
- `user_tracking/` - User tracking implementation
  - `user_tracking_strategy.py` - Base strategy interface
  - `role_based_tracker.py` - Tracks users based on Discord roles
  - `pinned_message_emoji_tracker.py` - Tracks users via pinned message reactions
  - `user_tracking_manager.py` - Manages multiple tracking strategies
- `summarize.py` - Provides message summarization strategies
- `google_vertex.py` - Integration with Google Vertex AI

## Setting Up a Discord Bot

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a new application
3. Navigate to the "Bot" tab and click "Add Bot"
4. Copy the token and add it to your `.env` file
5. Under "Privileged Gateway Intents", enable:
   - Message Content Intent
   - Server Members Intent
   - Presence Intent
6. Navigate to the "OAuth2" tab
7. Select "bot" and "applications.commands" scopes
8. Select the required permissions in the "Bot Permissions" section
9. Use the generated URL to invite the bot to your server 