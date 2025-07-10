from src.models.bot.resources.user import User
from src.models.base import BaseResourceObject

__all__ = ['SoundboardSound']

class SoundboardSound(BaseResourceObject):
    __slots__ = (
                    'name',
                    'sound_id',
                    'volume',
                    'emoji_id',
                    'emoji_name',
                    'guild_id',
                    'available',
                    'user'
                )
    
    def __init__(self, **kwargs):
        self.name: str           = kwargs.get('name')
        self.sound_id: str       = kwargs.get('sound_id')
        self.volume: int         = kwargs.get('volume')
        self.emoji_id: str       = kwargs.get('emoji_id')
        self.emoji_name: str     = kwargs.get('emoji_name')
        self.guild_id: str       = kwargs.get('guild_id', None)
        self.available: bool     = kwargs.get('available')
        self.user: User          = User(**kwargs.get('user')) if 'user' in kwargs and kwargs['user'] is not None else None

