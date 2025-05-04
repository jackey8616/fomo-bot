from abc import ABC, abstractmethod
from typing import List, Union

from discord import Guild, Member, User


class UserTrackingStrategy(ABC):
    """Abstract base class for user tracking strategies"""

    @abstractmethod
    async def find_users_to_track(
        self,
        guild: Guild,
        channel_id: int,
    ) -> List[Union[User, Member]]:
        """
        Determines which users should be tracked based on server-wide criteria

        Args:
            guild: The Discord guild (server) to search in

        Returns:
            A list of tuples containing (channel, list_of_users_to_track)
        """
        raise NotImplementedError("Subclasses must implement this method")
