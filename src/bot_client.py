from dataclasses import dataclass
from discord import Forbidden, TextChannel, Message, User, Embed, Color, utils
from discord.ext import commands

from google_vertex import GoogleVertexService
from summarize import summarize

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

    async def get_messages_base_on_whitelist(self, channel_id: int, user_ids: set[int]):
        channel = self.get_channel(channel_id)
        if channel is None:
            return []
        elif isinstance(channel, TextChannel) is False:
            return []
        assert isinstance(channel, TextChannel)

        messages = []
        async for message in channel.history(limit=100):
            assert isinstance(message, Message)
            if len(message.content) == 0 or message.author.id not in user_ids:
                continue
            messages.append((message.author, message.content))
        messages.reverse()
        return messages

    async def summarize_messages(self, messages: list[tuple[User, str]]):
        system_instructions, user_instructions = summarize(messages)
        return self.google_vertex_service.chat(
            model_name="gemini-2.0-flash-001",
            system_instructions=system_instructions,
            content=user_instructions)

class CommandsCog(commands.Cog):
    def __init__(self, bot: BotClient):
        self.bot = bot

    @commands.command(name='history')
    async def history(self, ctx):
        """Shows the history of messages from whitelisted users"""
        if not self.bot.channel_whitelist:
            await ctx.send("No whitelisted messages found!")
            return

        user_ids = set([user.id for user in self.bot.channel_whitelist[0][1]])
        messages = await self.bot.get_messages_base_on_whitelist(self.bot.channel_whitelist[0][0], user_ids)
        
        if not messages:
            await ctx.send("No messages found from whitelisted users!")
            return
        
        # Create an embed
        embed = Embed(
            title="📜 Message History",
            description="Here are the recent messages from whitelisted users:",
            color=Color.blue()
        )
        
        # Add messages to the embed
        for author, content in messages[:25]:  # Limit to 25 messages to avoid embed limits
            # Truncate long messages to fit in embed
            if len(content) > 1024:
                content = content[:1021] + "..."
            
            embed.add_field(
                name=f"👤 {author.name}",
                value=content,
                inline=False
            )
        
        # Add timestamp
        embed.set_footer(text="Last updated")
        embed.timestamp = utils.utcnow()
        
        await ctx.send(embed=embed)

    @commands.command(name='summarize')
    async def summarize(self, ctx):
        """Summarizes the messages from whitelisted users"""
        if not self.bot.channel_whitelist:
            await ctx.send("No whitelisted messages found!")
            return

        user_ids = set([user.id for user in self.bot.channel_whitelist[0][1]])
        messages = await self.bot.get_messages_base_on_whitelist(self.bot.channel_whitelist[0][0], user_ids)
        summary = await self.bot.summarize_messages(messages)
        await ctx.send(summary)
