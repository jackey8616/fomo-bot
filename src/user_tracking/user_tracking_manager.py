from typing import List, Optional, Set, Union

from discord import Guild, Member, User

from .user_tracking_strategy import UserTrackingStrategy


class UserTrackingManager:
    """Manager class that applies user tracking strategies to determine which users to track"""

    def __init__(self, strategies: Optional[List[UserTrackingStrategy]] = None):
        self.strategies: List[UserTrackingStrategy] = (
            strategies if strategies is not None else []
        )

    def add_strategy(self, strategy: UserTrackingStrategy):
        """Add a new strategy to the manager"""
        self.strategies.append(strategy)

    async def find_users_to_track(
        self,
        guild: Guild,
        channel_id: int,
    ) -> Set[Union[User, Member]]:
        """
        Process a guild through all strategies to find users to track

        Args:
            guild: The Discord guild to process

        Returns:
            List of tuples containing (channel_id, list_of_users)
        """
        result: Set[Union[User, Member]] = set()

        # Apply all strategies
        for strategy in self.strategies:
            strategy_results = await strategy.find_users_to_track(guild, channel_id)
            result.update(strategy_results)

        return result
