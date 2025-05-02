from typing import List, Tuple, Union

from discord import Forbidden, Guild, Member, TextChannel, User

from .user_tracking_strategy import UserTrackingStrategy


class PinnedMessageEmojiTracker(UserTrackingStrategy):
    """Strategy for tracking users who reacted with a specific emoji to a whitelist message"""

    def __init__(self, whitelist_keyword: str = "FomoBot TrackList", emoji: str = "✅"):
        self.whitelist_keyword = whitelist_keyword
        self.emoji = emoji

    async def find_users_to_track(
        self, guild: Guild
    ) -> List[Tuple[TextChannel, List[Union[User, Member]]]]:
        """
        Find users to track by scanning pinned messages across all channels in the guild

        Args:
            guild: The Discord guild to search in

        Returns:
            A list of tuples containing (channel, list_of_users_to_track)
        """
        result = []

        for channel in guild.text_channels:
            try:
                pinned_messages = await channel.pins()

                for partial_message in pinned_messages:
                    # Fetch the full message to get reactions
                    message = await channel.fetch_message(partial_message.id)

                    # Check if this is a whitelist message
                    if self.whitelist_keyword not in message.content:
                        continue

                    # Check reactions for the whitelist emoji
                    users_to_track = []
                    for reaction in message.reactions:
                        if reaction.emoji == self.emoji:
                            # Get all users who reacted with this emoji
                            users = [user async for user in reaction.users()]
                            users_to_track.extend(users)

                    # If we found users to track, add to results
                    if users_to_track:
                        result.append((channel, users_to_track))

            except Forbidden:
                print(f"Don't have permission to read pins in {channel.name}")
            except Exception as e:
                print(f"Error scanning channel {channel.name}: {str(e)}")

        return result
