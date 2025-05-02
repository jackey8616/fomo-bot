from typing import List, Tuple, Union
from discord import User, Member, Guild, TextChannel

from .user_tracking_strategy import UserTrackingStrategy


class RoleBasedTracker(UserTrackingStrategy):
    """Strategy that tracks users with specific roles across the guild"""
    
    def __init__(self, role_names: List[str]):
        self.role_names = role_names
        
    async def find_users_to_track(self, guild: Guild) -> List[Tuple[TextChannel, List[Union[User, Member]]]]:
        """
        Find users to track based on their roles in the guild
        
        Args:
            guild: The Discord guild to search in
            
        Returns:
            A list of tuples containing (channel, list_of_users_to_track)
        """
        # Find all members with the specified roles
        users_to_track = []
        relevant_roles = []
        
        # Find the roles we're interested in
        for role in guild.roles:
            if role.name in self.role_names:
                relevant_roles.append(role)
        
        # If we didn't find any matching roles, return empty result
        if not relevant_roles:
            return []
        
        # Find members with those roles
        for member in guild.members:
            member_roles = set(member.roles)

            if any(role in member_roles for role in relevant_roles):
                users_to_track.append(member)
        
        # Add to every channel
        result = []
        for channel in guild.channels:
            result.append((channel, users_to_track))

        return result 