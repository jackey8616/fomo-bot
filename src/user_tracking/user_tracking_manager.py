from typing import List, Tuple, Optional, Union, Set, Dict
from collections import defaultdict
from discord import User, Member, Guild, TextChannel

from .user_tracking_strategy import UserTrackingStrategy


class UserTrackingManager:
    """Manager class that applies user tracking strategies to determine which users to track"""
    
    def __init__(self, strategies: Optional[List[UserTrackingStrategy]] = None):
        self.strategies: List[UserTrackingStrategy] = strategies if strategies is not None else []
        
    def add_strategy(self, strategy: UserTrackingStrategy):
        """Add a new strategy to the manager"""
        self.strategies.append(strategy)
        
    async def find_users_to_track(self, guild: Guild) -> List[Tuple[int, List[Union[User, Member]]]]:
        """
        Process a guild through all strategies to find users to track
        
        Args:
            guild: The Discord guild to process
            
        Returns:
            List of tuples containing (channel_id, list_of_users)
        """
        # Dictionary to track users by channel
        channel_users: Dict[TextChannel, Set[Union[User, Member]]] = defaultdict(set)
        
        # Apply all strategies
        for strategy in self.strategies:
            strategy_results = await strategy.find_users_to_track(guild)
            
            # Combine results from this strategy
            for channel, users in strategy_results:
                channel_users[channel].update(users)
        
        # Convert to the expected return format
        result = []
        for channel, users in channel_users.items():
            if users:  # Only include channels with users to track
                result.append((channel.id, list(users)))
                
        return result 