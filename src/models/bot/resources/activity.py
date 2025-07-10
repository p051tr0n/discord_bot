from typing import List
from typing_extensions import Optional

from src.models.base import BaseResourceObject


__all__ = ['Activity', 'ActivityButton','ActivityEmoji', 'ActivityAssets', 'ActivityParty', 'ActivitySecrets', 'ActivityTimestamps']

#-----------------------------------------------------------------------------------------------------------------
class ActivityParty(BaseResourceObject):
    __slots__ = (
        'id',
        'size')

    def __init__(self, **kwargs):
        self.id: str            = kwargs.get('id')
        self.size: List[int]    = kwargs.get('size')

#-----------------------------------------------------------------------------------------------------------------
class ActivityEmoji(BaseResourceObject):
    __slots__ = (
        'name',
        'id',
        'animated')

    def __init__(self, **kwargs):
        self.name: str                  = kwargs.get('name')
        self.id: Optional[str]          = kwargs.get('id')
        self.animated: Optional[bool]   = kwargs.get('animated')

#-----------------------------------------------------------------------------------------------------------------
class ActivityAssets(BaseResourceObject):
    __slots__ = (
        'large_image',
        'large_text',
        'small_image',
        'small_text')

    def __init__(self, **kwargs):
        self.large_image: str   = kwargs.get('large_image')
        self.large_text: str    = kwargs.get('large_text')
        self.small_image: str   = kwargs.get('small_image')
        self.small_text: str    = kwargs.get('small_text')

#-----------------------------------------------------------------------------------------------------------------
class ActivitySecrets(BaseResourceObject):
    __slots__ = (
        'join',
        'spectate',
        'match')

    def __init__(self, **kwargs):
        self.join: str      = kwargs.get('join')
        self.spectate: str  = kwargs.get('spectate')
        self.match: str     = kwargs.get('match')

#-----------------------------------------------------------------------------------------------------------------
class ActivityButton(BaseResourceObject):
    __slots__ = (
        'label',
        'url')

    def __init__(self, **kwargs):
        self.label: str     = kwargs.get('label')
        self.url: str       = kwargs.get('url')

#-----------------------------------------------------------------------------------------------------------------
class ActivityTimestamps(BaseResourceObject):
    __slots__ = (
        'start',
        'end')

    def __init__(self, **kwargs):
        self.start: int     = kwargs.get('start')
        self.end: int       = kwargs.get('end')

#-----------------------------------------------------------------------------------------------------------------
class Activity(BaseResourceObject):
    __slots__ = (
        'name',
        'type',
        'url',
        'created_at',
        'timestamps',
        'application_id',
        'details',
        'state',
        'emoji',
        'party',
        'assets',
        'secrets',
        'instance',
        'flags',
        'buttons')

    def __init__(self, **kwargs):
        self.name: str                                  = kwargs.get('name')
        self.type: int                                  = kwargs.get('type')
        self.url: Optional[str]                         = kwargs.get('url', None)
        self.created_at: int                            = kwargs.get('created_at')
        self.timestamps: Optional[ActivityTimestamps]   = ActivityTimestamps(**kwargs.get('timestamps')) if 'timestamps' in kwargs and kwargs['timestamps'] is not None else None
        self.application_id: Optional[str]              = kwargs.get('application_id', None)
        self.details: Optional[str]                     = kwargs.get('details', None)
        self.state: Optional[str]                       = kwargs.get('state', None)
        self.emoji: Optional[ActivityEmoji]             = ActivityEmoji(**kwargs.get('emoji')) if 'emoji' in kwargs and kwargs['eomji'] is not None else None
        self.party: Optional[ActivityParty]             = ActivityParty(**kwargs.get('party')) if 'party' in kwargs and kwargs['party'] is not None else None
        self.assets: Optional[ActivityAssets]           = ActivityAssets(**kwargs.get('assets')) if 'assets' in kwargs and kwargs['assets'] is not None else None
        self.secrets: Optional[ActivitySecrets]         = ActivitySecrets(**kwargs.get('secrets')) if 'secrets' in kwargs and kwargs['secrets'] is not None else None
        self.instance: Optional[bool]                   = kwargs.get('instance', None)
        self.flags: Optional[int]                       = kwargs.get('flags', None)
        self.buttons: Optional[List[ActivityButton]]    = [ActivityButton(**x) for x in kwargs.get('buttons')] if 'buttons' in kwargs and kwargs['button'] is not None else None
