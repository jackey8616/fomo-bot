from abc import ABC, abstractmethod
from typing import List, Tuple, Union

from discord import Guild, Member, TextChannel, User


class UserTrackingStrategy(ABC):
    """Abstract base class for user tracking strategies"""

    @abstractmethod
    async def find_users_to_track(
        self, guild: Guild
    ) -> List[Tuple[TextChannel, List[Union[User, Member]]]]:
        """
        Determines which users should be tracked based on server-wide criteria

        Args:
            guild: The Discord guild (server) to search in

        Returns:
            A list of tuples containing (channel, list_of_users_to_track)
        """
        raise NotImplementedError("Subclasses must implement this method")
