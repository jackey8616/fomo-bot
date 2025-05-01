from discord import Intents
from os import getenv
from dotenv import load_dotenv
from bot_client import BotClient

# Load environment variables
load_dotenv(override=True)

# Bot setup
intents = Intents.default()
intents.message_content = True
intents.reactions = True  # Enable reaction intents

# Initialize the bot with command prefix
client = BotClient(command_prefix='!', intents=intents)

# Run the bot
token = getenv('DISCORD_TOKEN')
if token is None:
    raise ValueError("DISCORD_TOKEN environment variable is not set")
client.run(token)
