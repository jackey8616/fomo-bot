from dataclasses import dataclass
from typing import List, Optional, Union

import pytz
from discord import Interaction, Member, Message, User, app_commands
from discord.abc import GuildChannel, Messageable
from discord.ext.commands import Bot, Cog

from google_vertex import GoogleVertexService
from summarize import casual_summarize, serious_summarize_with_link
from user_tracking import RoleBasedTracker, UserTrackingManager


@dataclass
class BotClient(Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.channel_whitelist: list[tuple[int, list[Union[User, Member]]]] = []
        self.google_vertex_service = GoogleVertexService()
        self.user_tracking_manager = UserTrackingManager()

        # Add user tracking strategies
        self.user_tracking_manager.add_strategy(RoleBasedTracker(["FomoTrack"]))

    async def setup_hook(self):
        await self.add_cog(CommandsCog(self))
        # Sync application commands with Discord
        print("Syncing application commands...")
        await self.tree.sync()
        print("Application commands synced.")

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
        async for message in channel.history(limit=300):
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
        system_instructions, user_instructions = serious_summarize_with_link(messages)
        output = self.google_vertex_service.chat(
            model_name="gemini-2.0-flash-001",
            content=user_instructions,
            system_instructions=system_instructions,
        )

        for each in messages:
            in_output_url = f"[Ref]({each.id})"
            if in_output_url in output:
                output = output.replace(in_output_url, f"{each.jump_url}")

        return output


class CommandsCog(Cog):
    def __init__(self, bot: BotClient):
        self.bot = bot

    @app_commands.command(
        name="casual_summarize",
        description="Summarizes the messages from whitelisted users in a casual format",
    )
    @app_commands.describe(
        channel="The channel to summarize messages from. If not provided, uses the current channel."
    )
    async def casual_summarize(
        self, interaction: Interaction, channel: Optional[GuildChannel] = None
    ):
        """Summarizes the messages from whitelisted users in a casual format"""
        if not self.bot.channel_whitelist:
            await interaction.response.send_message("No whitelisted messages found!")
            return

        # Use provided channel or current channel
        target_channel = channel or interaction.channel
        if target_channel is None:
            await interaction.response.send_message(
                "Could not determine the channel to summarize."
            )
            return

        channel_id = target_channel.id
        channel_url = target_channel.jump_url
        user_ids = {user.id for user in self.bot.channel_whitelist[0][1]}

        await interaction.response.defer(thinking=True)

        messages = await self.bot.get_messages_base_on_whitelist(channel_id, user_ids)

        if not messages:
            await interaction.followup.send(
                f"No whitelisted messages found in channel {channel_url}!"
            )
            return

        result = await self.bot.casual_summarize_messages(messages)

        # Convert timestamps to TZ+8
        tz = pytz.timezone("Asia/Taipei")  # TZ+8 timezone
        start_time = messages[0].created_at.replace(tzinfo=pytz.UTC).astimezone(tz)
        end_time = messages[-1].created_at.replace(tzinfo=pytz.UTC).astimezone(tz)
        timestamp_info = f"**Casual Summary** for channel {channel_url}\n\n摘要起點: {start_time.strftime('%Y-%m-%d %H:%M:%S')} (UTC+8)\n摘要終點: {end_time.strftime('%Y-%m-%d %H:%M:%S')} (UTC+8)"
        output = f"{timestamp_info}\n{result}"

        await self._chunk_send(interaction, output)

    @app_commands.command(
        name="serious_summarize",
        description="Summarizes the messages from whitelisted users in a detailed format",
    )
    @app_commands.describe(
        channel="The channel to summarize messages from. If not provided, uses the current channel."
    )
    async def serious_summarize(
        self, interaction: Interaction, channel: Optional[GuildChannel] = None
    ):
        """Summarizes the messages from whitelisted users in a detailed format"""
        if not self.bot.channel_whitelist:
            await interaction.response.send_message("No whitelisted messages found!")
            return

        # Use provided channel or current channel
        target_channel = channel or interaction.channel
        if target_channel is None:
            await interaction.response.send_message(
                "Could not determine the channel to summarize."
            )
            return

        channel_id = target_channel.id
        channel_url = target_channel.jump_url
        user_ids = {user.id for user in self.bot.channel_whitelist[0][1]}

        await interaction.response.defer(thinking=True)

        messages = await self.bot.get_messages_base_on_whitelist(channel_id, user_ids)

        if not messages:
            await interaction.followup.send(
                f"No whitelisted messages found in channel {channel_url}!"
            )
            return

        result = await self.bot.serious_summarize_messages(messages)

        # Convert timestamps to TZ+8
        tz = pytz.timezone("Asia/Taipei")  # TZ+8 timezone
        start_time = messages[0].created_at.replace(tzinfo=pytz.UTC).astimezone(tz)
        end_time = messages[-1].created_at.replace(tzinfo=pytz.UTC).astimezone(tz)
        timestamp_info = f"**Serious Summary** for channel {channel_url}\n\n摘要起點: {start_time.strftime('%Y-%m-%d %H:%M:%S')} (UTC+8)\n摘要終點: {end_time.strftime('%Y-%m-%d %H:%M:%S')} (UTC+8)"
        output = f"{timestamp_info}\n{result}"

        await self._chunk_send(interaction, output)

    async def _chunk_send(
        self, interaction: Interaction, content: str, chunk_size: int = 1900
    ):
        # Split content by lines first
        lines = content.split("\n")
        chunks = []
        current_chunk = ""

        for line in lines:
            # If adding this line would exceed chunk size, start a new chunk
            if len(current_chunk) + len(line) + 1 > chunk_size:
                # If the line itself is longer than chunk_size, we need to split it
                if len(line) > chunk_size:
                    remaining_line = line
                    while remaining_line:
                        available_space = chunk_size - len(current_chunk)
                        if available_space <= 0:
                            chunks.append(current_chunk)
                            current_chunk = ""
                            available_space = chunk_size

                        chunk_part = remaining_line[:available_space]
                        remaining_line = remaining_line[available_space:]

                        if current_chunk:
                            current_chunk += "\n" + chunk_part
                        else:
                            current_chunk = chunk_part

                        if len(current_chunk) >= chunk_size:
                            chunks.append(current_chunk)
                            current_chunk = ""
                else:
                    # Add current chunk to chunks and start a new one with this line
                    chunks.append(current_chunk)
                    current_chunk = line
            else:
                # Add line to current chunk
                if current_chunk:
                    current_chunk += "\n" + line
                else:
                    current_chunk = line

        # Add the last chunk if it's not empty
        if current_chunk:
            chunks.append(current_chunk)

        # Send all chunks
        for i, chunk in enumerate(chunks):
            if i == 0:
                await interaction.followup.send(chunk)
            else:
                await interaction.followup.send(chunk)
