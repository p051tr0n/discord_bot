from models.base import BaseResourceObject

__all__ = ['StageInstance']

class StageInstance(BaseResourceObject):
    __slots__ = (
                    'id',
                    'guild_id',
                    'channel_id',
                    'topic',
                    'privacy_level',
                    'discoverable_disabled',
                    'guild_scheduled_event_id'
                )
    
    def __init__(self, **kwargs):
        self.id: str                    = kwargs.get('id')
        self.guild_id: str              = kwargs.get('guild_id')
        self.channel_id: str            = kwargs.get('channel_id')
        self.topic: str                 = kwargs.get('topic')
        self.privacy_level: int         = kwargs.get('privacy_level')
        self.discoverable_disabled: bool= kwargs.get('discoverable_disabled')
        self.guild_scheduled_event_id   = kwargs.get('guild_scheduled_event_id', None)