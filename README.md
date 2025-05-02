# FOMO Bot

A Discord bot that monitors whitelisted messages in channels and provides summarization features.

## Features

- Multiple user tracking strategies:
  - Role-based tracking: Tracks users with the "FomoTrack" role across the guild
  - Pinned message tracking: Scans pinned messages for "FomoBot TrackList" keyword and tracks users who react with ✅
- Provides two summarization modes:
  - Casual summarization (`!casual_summarize`) - Quick, concise summary of recent messages
  - Serious summarization (`!serious_summarize`) - Detailed, structured summary with key learnings, shared resources, help exchanges, and project updates
- Integration with Google Vertex AI (Gemini) for message summarization
- Flexible architecture with dependency injection using Kink

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

## Usage

### Setting Up User Tracking

#### Role-Based Tracking
The bot tracks users with the "FomoTrack" role by default. Users with this role will be monitored in all channels.

#### Pinned Message Tracking
1. Create a pinned message in a channel with the content containing "FomoBot TrackList"
2. React to this message with a ✅ emoji
3. Any users who add a ✅ reaction to this message will be tracked

### Bot Commands

- `!casual_summarize [channel]` - Generates a concise summary of the conversation in a casual format. Optionally specify a channel to summarize.
- `!serious_summarize [channel]` - Generates a detailed, structured summary of the conversation including key learnings, shared resources, help exchanges, and project updates. Optionally specify a channel to summarize.

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

## Project Architecture

The project uses:
- Python 3.13
- discord.py 2.3.2
- Kink for dependency injection
- Google Cloud Vertex AI
- Poetry for dependency management

### Key Components

- `bot_client.py` - Main Discord bot implementation with command handling
- `user_tracking/` - Strategies for tracking users in channels
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
7. Use the OAuth2 URL Generator to create an invite link with appropriate permissions 