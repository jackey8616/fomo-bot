from dataclasses import dataclass
from typing import List, Union

from discord import Color, Embed, Member, Message, User
from discord.abc import Messageable
from discord.ext import commands

from google_vertex import GoogleVertexService
from summarize import casual_summarize, serious_summarize
from user_tracking import RoleBasedTracker, UserTrackingManager


@dataclass
class BotClient(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.channel_whitelist: list[tuple[int, list[Union[User, Member]]]] = []
        self.google_vertex_service = GoogleVertexService()
        self.user_tracking_manager = UserTrackingManager()

        # Add user tracking strategies
        self.user_tracking_manager.add_strategy(RoleBasedTracker(["AAA"]))

    async def setup_hook(self):
        await self.add_cog(CommandsCog(self))

    async def on_ready(self):
        self.channel_whitelist = await self.refresh_user_tracking()
        print(f"{self.user} has connected to Discord!")

    async def refresh_user_tracking(
        self,
    ) -> List[tuple[int, list[Union[User, Member]]]]:
        """
        Refresh the list of users to track by scanning all guilds

        Returns:
            List of tuples containing (channel_id, list_of_users)
        """
        print("Starting user tracking refresh...")
        all_tracked_users = []

        for guild in self.guilds:
            guild_tracked_users = await self.user_tracking_manager.find_users_to_track(
                guild
            )
            all_tracked_users.extend(guild_tracked_users)

        return all_tracked_users

    async def get_messages_base_on_whitelist(
        self, channel_id: int, user_ids: set[int]
    ) -> list[Message]:
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
            system_instructions=system_instructions,
        )

    async def serious_summarize_messages(self, messages: list[Message]):
        system_instructions, user_instructions = serious_summarize(messages)
        return self.google_vertex_service.chat(
            model_name="gemini-2.0-flash-001",
            content=user_instructions,
            system_instructions=system_instructions,
        )


class CommandsCog(commands.Cog):
    def __init__(self, bot: BotClient):
        self.bot = bot

    @commands.command(name="casual_summarize")
    async def casual_summarize(self, ctx):
        """Summarizes the messages from whitelisted users"""
        if not self.bot.channel_whitelist:
            await ctx.send("No whitelisted messages found!")
            return

        # channel_id = self.bot.channel_whitelist[0][0]
        channel_id = ctx.channel.id
        user_ids = {user.id for user in self.bot.channel_whitelist[0][1]}
        messages = await self.bot.get_messages_base_on_whitelist(channel_id, user_ids)
        summary = await self.bot.casual_summarize_messages(messages)

        # Create an embed for better formatting
        embed = Embed(title="Casual Summary", description=summary, color=Color.blue())
        await ctx.send(embed=embed)

    @commands.command(name="serious_summarize")
    async def serious_summarize(self, ctx):
        """Summarizes the messages from whitelisted users"""
        if not self.bot.channel_whitelist:
            await ctx.send("No whitelisted messages found!")
            return

        # channel_id = self.bot.channel_whitelist[0][0]
        channel_id = ctx.channel.id
        user_ids = {user.id for user in self.bot.channel_whitelist[0][1]}
        messages = await self.bot.get_messages_base_on_whitelist(channel_id, user_ids)
        summary = await self.bot.serious_summarize_messages(messages)

        # Create an embed for better formatting
        embed = Embed(
            title="Serious Summary", description=summary, color=Color.dark_green()
        )
        await ctx.send(embed=embed)
