from src.models.bot.resources.user import GuildMember
from src.models.base import BaseResourceObject

__all__ = ['VoiceState']

class VoiceState(BaseResourceObject):
    __slots__ = (
                    'guild_id',
                    'channel_id',
                    'user_id',
                    'member',
                    'session_id',
                    'deaf',
                    'mute',
                    'self_deaf',
                    'self_mute',
                    'self_stream',
                    'self_video',
                    'suppress',
                    'request_to_speak_timestamp'
                )
    
    def __init__(self, **kwargs):
        self.guild_id                   = kwargs.get('guild_id', None)
        self.channel_id                 = kwargs.get('channel_id')
        self.user_id                    = kwargs.get('user_id')
        self.member                     = GuildMember(**kwargs.get('member')) if 'member' in kwargs and kwargs['member'] is not None else None
        self.session_id                 = kwargs.get('session_id', None)
        self.deaf                       = kwargs.get('deaf', False)
        self.mute                       = kwargs.get('mute', False)
        self.self_deaf                  = kwargs.get('self_deaf', False)
        self.self_mute                  = kwargs.get('self_mute', False)
        self.self_stream                = kwargs.get('self_stream', None)
        self.self_video                 = kwargs.get('self_video', False)
        self.suppress                   = kwargs.get('suppress', False)
        self.request_to_speak_timestamp = kwargs.get('request_to_speak_timestamp', None)