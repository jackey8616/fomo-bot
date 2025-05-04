from typing import List, Union

from discord import Forbidden, Guild, Member, User
from discord.abc import Messageable

from .user_tracking_strategy import UserTrackingStrategy


class PinnedMessageEmojiTracker(UserTrackingStrategy):
    """Strategy for tracking users who reacted with a specific emoji to a tracking message"""

    def __init__(self, tracking_keyword: str = "FomoBot TrackList", emoji: str = "✅"):
        self.tracking_keyword = tracking_keyword
        self.emoji = emoji

    async def find_users_to_track(
        self,
        guild: Guild,
        channel_id: int,
    ) -> List[Union[User, Member]]:
        """
        Find users to track by scanning pinned messages across all channels in the guild

        Args:
            guild: The Discord guild to search in

        Returns:
            A list of tuples containing (channel, list_of_users_to_track)
        """
        users_to_track: List[Union[User, Member]] = []
        channel = guild.get_channel(channel_id)

        if channel is None:
            return []
        elif isinstance(channel, Messageable) is False:
            return []

        assert isinstance(channel, Messageable)
        try:
            pinned_messages = await channel.pins()

            for partial_message in pinned_messages:
                # Fetch the full message to get reactions
                message = await channel.fetch_message(partial_message.id)

                # Check if this is a tracking message
                if self.tracking_keyword not in message.content:
                    continue

                for reaction in message.reactions:
                    if reaction.emoji == self.emoji:
                        # Get all users who reacted with this emoji
                        users = [user async for user in reaction.users()]
                        users_to_track.extend(users)
        except Forbidden:
            print(f"Don't have permission to read pins in {channel.name}")
        except Exception as e:
            print(f"Error scanning channel {channel.name}: {str(e)}")

        return users_to_track
