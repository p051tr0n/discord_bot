
from src.models.bot.resources.user import User, GuildMember
from src.models.bot.resources.activity import Activity
from src.models.base import BaseResourceObject

from typing import List, Optional

__all__ = ['ClientStatus', 'Presence', 'Typing']

class ClientStatus(BaseResourceObject):
    __slots__ = (
                    'desktop',
                    'mobile',
                    'web'
                )
    def __init__(self, **kwargs):
        self.desktop = kwargs.pop('desktop', '')
        self.mobile = kwargs.pop('mobile', '')
        self.web = kwargs.pop('web', '')

class Presence(BaseResourceObject):
    __slots__ = (
                    'user',
                    'guild_id',
                    'status',
                    'activities',
                    'client_status'
                )
    
    def __init__(self, **kwargs):
        self.user: User                     = User(**kwargs.get('user'))
        self.guild_id: str                  = kwargs.get('guild_id')
        self.status: str                    = kwargs.get('status')
        self.activities: List[Activity]     = [Activity(**x) for x in kwargs.get('activities')] if 'activities' in kwargs and kwargs['activities'] is not None else []
        self.client_status: ClientStatus    = ClientStatus(**kwargs.get('client_status'))

class Typing(BaseResourceObject):
    __slots__ = (
                    'channel_id',
                    'guild_id',
                    'user_id',
                    'timestamp',
                    'member'
                )

    def __init__(self, **kwargs):
        self.user_id: str                   = kwargs.get('user_id')
        self.timestamp: int                 = kwargs.get('timestamp')
        self.guild_id: Optional[str]        = kwargs.get('guild_id', None)
        self.channel_id: str                = kwargs.get('channel_id')
        self.member: Optional[GuildMember]  = GuildMember(**kwargs.get('member')) if 'member' in kwargs and kwargs['member'] is not None else None