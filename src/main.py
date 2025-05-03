from discord import Intents
from kink import di

from bootstrap import bootstrap
from bot_client import BotClient

# Load environment variables
bootstrap()

# Bot setup
intents = Intents.default()
intents.message_content = True
intents.members = True
intents.reactions = True

# Initialize the bot with command_prefix but we'll use application commands (slash commands)
client = BotClient(command_prefix="!", intents=intents)

# Run the bot
token = di["DISCORD_TOKEN"]
client.run(token)
