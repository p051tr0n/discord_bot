from typing import List
from typing_extensions import Optional

from src.models.bot.resources.user import User
from src.models.base import BaseResourceObject


__all__ = ['Sticker']

class Sticker(BaseResourceObject):
    __slots__ = (
        'id',
        'pack_id',
        'name',
        'description',
        'tags',
        'type',
        'format_type',
        'available',
        'guild_id',
        'user',
        'sort_value'
    )

    def __init__(self, **kwargs):
        self.id: str                    = kwargs.get('id')
        self.pack_id: Optional[str]     = kwargs.get('pack_id', None)
        self.name: str                  = kwargs.get('name')
        self.description: str           = kwargs.get('description')
        self.tags: str                  = kwargs.get('tags')
        self.type: int                  = kwargs.get('type')
        self.format_type: int           = kwargs.get('format_type')
        self.available: Optional[bool]  = kwargs.get('available', None)
        self.guild_id: Optional[str]    = kwargs.get('guild_id', None)
        self.user: Optional[User]       = User(**kwargs.get('user')) if 'user' in kwargs and kwargs['user'] is not None else None
        self.sort_value: Optional[int]  = kwargs.get('sort_value', None)