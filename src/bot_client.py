from dataclasses import dataclass
from discord import Forbidden, Message, User, Embed, Color
from discord.abc import Messageable
from discord.ext import commands

from google_vertex import GoogleVertexService
from summarize import casual_summarize, serious_summarize

@dataclass
class BotClient(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.channel_whitelist: list[tuple[int, list[User]]] = []
        self.google_vertex_service = GoogleVertexService()
        
    async def setup_hook(self):
        await self.add_cog(CommandsCog(self))

    async def on_ready(self):
        self.channel_whitelist = await self.scan_pinned_messages()
        print(f'{self.user} has connected to Discord!')
    
    async def scan_pinned_messages(self):
        print("Starting pinned messages scan...")
        channel_whitelist = []
        for guild in self.guilds:
            for channel in guild.text_channels:
                try:
                    pinned_partial_messages = await channel.pins()
                    
                    for partial_message in pinned_partial_messages:
                        if "FomoBot Whitelist" in partial_message.content:
                            message = await channel.fetch_message(partial_message.id)
                            reactions = message.reactions
                            
                            if len(reactions) == 0:
                                continue

                            for reaction in reactions:
                                if reaction.emoji == "✅":
                                    channel_whitelist.append((channel.id, [user async for user in reaction.users()]))
                except Forbidden:
                    print(f"Don't have permission to read pins in {channel.name}")
                except Exception as e:
                    print(f"Error scanning channel {channel.name}: {str(e)}")
        return channel_whitelist

    async def get_messages_base_on_whitelist(self, channel_id: int, user_ids: set[int]) -> list[Message]:
        channel = self.get_channel(channel_id)
        if channel is None:
            return []
        assert isinstance(channel, Messageable)

        messages = []
        async for message in channel.history(limit=100):
            assert isinstance(message, Message)
            if len(message.content) == 0 or message.author.id not in user_ids:
                continue
            messages.append(message)
        messages.reverse()
        return messages

    async def casual_summarize_messages(self, messages: list[Message]):
        system_instructions, user_instructions = casual_summarize(messages)
        return self.google_vertex_service.chat(
            model_name="gemini-2.0-flash-001",
            content=user_instructions,
            system_instructions=system_instructions)

    async def serious_summarize_messages(self, messages: list[Message]):
        system_instructions, user_instructions = serious_summarize(messages)
        return self.google_vertex_service.chat(
            model_name="gemini-2.0-flash-001",
            content=user_instructions,
            system_instructions=system_instructions)


class CommandsCog(commands.Cog):
    def __init__(self, bot: BotClient):
        self.bot = bot

    @commands.command(name='casual_summarize')
    async def casual_summarize(self, ctx):
        """Summarizes the messages from whitelisted users"""
        if not self.bot.channel_whitelist:
            await ctx.send("No whitelisted messages found!")
            return

        # channel_id = self.bot.channel_whitelist[0][0]
        channel_id = ctx.channel.id
        user_ids = set([user.id for user in self.bot.channel_whitelist[0][1]])
        messages = await self.bot.get_messages_base_on_whitelist(channel_id, user_ids)
        summary = await self.bot.casual_summarize_messages(messages)
        
        # Create an embed for better formatting
        embed = Embed(
            title="Casual Summary",
            description=summary,
            color=Color.blue()
        )
        await ctx.send(embed=embed)
    
    @commands.command(name='serious_summarize')
    async def serious_summarize(self, ctx):
        """Summarizes the messages from whitelisted users"""
        if not self.bot.channel_whitelist:
            await ctx.send("No whitelisted messages found!")
            return

        # channel_id = self.bot.channel_whitelist[0][0]
        channel_id = ctx.channel.id
        user_ids = set([user.id for user in self.bot.channel_whitelist[0][1]])
        messages = await self.bot.get_messages_base_on_whitelist(channel_id, user_ids)
        summary = await self.bot.serious_summarize_messages(messages)
        
        # Create an embed for better formatting
        embed = Embed(
            title="Serious Summary",
            description=summary,
            color=Color.dark_green()
        )
        await ctx.send(embed=embed)
