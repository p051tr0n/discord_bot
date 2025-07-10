from src.models.base import BaseResourceObject
from src.obj_types.resource_types.snowflake import Snowflake

__all__ = ['Role', 'RoleTag']


class RoleTag(BaseResourceObject):
    __slots__ = ('bot_id', 'integration_id', 'premium_subscriber', 'subscription_listing_id', 'available_for_purchase', 'guild_connections')
    
    def __init__(self, **kwargs):
        self.bot_id                     = kwargs.get('bot_id', "")
        self.integration_id             = kwargs.get('integration_id', "")
        self.premium_subscriber         = kwargs.get('premium_subscriber', False)
        self.subscription_listing_id    = kwargs.get('subscription_listing_id', "")
        self.available_for_purchase     = kwargs.get('available_for_purchase', False)
        self.guild_connections          = kwargs.get('guild_connections', False)

class Role(BaseResourceObject):
    __slots__ = ('id', 'name', 'color', 'hoist', 'icon', 'unicode_emoji', 'position', 'permissions', 'managed', 'mentionable', 'tags', 'flags')
    def __init__(self, **kwargs):
        self.id             = kwargs.get('id', "")
        self.name           = kwargs.get('name', "")
        self.color          = kwargs.get('color', 0)
        self.hoist          = kwargs.get('hoist', False)
        self.icon           = kwargs.get('icon', None)
        self.unicode_emoji  = kwargs.get('unicode_emoji', None)
        self.position       = kwargs.get('position', 0)
        self.permissions    = kwargs.get('permissions', 0)
        self.managed        = kwargs.get('managed', False)
        self.mentionable    = kwargs.get('mentionable', False)
        self.tags           = RoleTag(**kwargs.get('tags')) if 'tags' in kwargs and kwargs['tags'] is not None else None
        self.flags          = kwargs.get('flags', 0)

