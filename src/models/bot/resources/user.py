from enum import Enum
from src.models.base import BaseResourceObject


__all__ = ['User', 'UserFlags', 'UserAvatarDecoration', 'GuildMember', 'GuildMemberAdd', 'GuildMemberRemove']

PremiumTypes = {
    0: 'None',
    1: 'Nitro Classic',
    2: 'Nitro',
    3: 'Nitro Basic'
}

class UserAvatarDecoration(BaseResourceObject):
    __slots__ = (
                    'asset',
                    'sku_id'
                )

    def __init__(self, **kwargs):
        self.asset = kwargs.pop('asset', '')
        self.sku_id = kwargs.pop('sku_id', '')


class User(BaseResourceObject):
    def __init__(self, **kwargs):
        '''
            Represents the User Structure defined here: https://discord.com/developers/docs/resources/User
        '''
        self.id                     = kwargs.pop('id', '')
        self.username               = kwargs.pop('username', '')
        self.discriminator          = kwargs.pop('discriminator', '')
        self.global_name            = kwargs.pop('global_name', '')
        self.avatar                 = kwargs.pop('avatar', '')
        self.bot                    = kwargs.pop('bot', None)
        self.system                 = kwargs.pop('system', None)
        self.mfa_enabled            = kwargs.pop('mfa_enabled', None)
        self.banner                 = kwargs.pop('banner', None)
        self.accent_color           = kwargs.pop('accent_color', None)
        self.locale                 = kwargs.pop('locale', None)
        self.verified               = kwargs.pop('verified', None)
        self.email                  = kwargs.pop('email', None)
        self.flags                  = kwargs.pop('flags', None)
        self.premium_type           = kwargs.pop('premium_type', None)
        self.public_flags           = kwargs.pop('public_flags', None)
        self.avatar_decoration_data = UserAvatarDecoration(**kwargs.pop('avatar_decoration_data')) if 'avatar_decoration_data' in kwargs and kwargs['avatar_decoration_data'] is not None else None


class PartialGuildMember(BaseResourceObject):
    __slots__  = ('roles', 
                    'premium_since', 
                    'pending', 
                    'nick',
                     'mute', 
                     'joined_at', 
                     'flags', 
                     'deaf', 
                     'communication_disabled_until', 
                     'banner', 
                     'avatar')
    def __init__(self, **kwargs):
        '''
            Represents the Partial Guild Member Structure defined here: https://discord.com/developers/docs/resources/guild
        '''
        self.roles = kwargs.pop('roles', [])
        self.premium_since = kwargs.pop('premium_since', None)
        self.pending = kwargs.pop('pending', False)
        self.nick = kwargs.pop('nick', None)
        self.mute = kwargs.pop('mute', False)
        self.joined_at = kwargs.pop('joined_at', None)
        self.flags = kwargs.pop('flags', 0)
        self.deaf = kwargs.pop('deaf', False)
        self.communication_disabled_until = kwargs.pop('communication_disabled_until', None)
        self.banner = kwargs.pop('banner', None)
        self.avatar = kwargs.pop('avatar', None)

class GuildMember(PartialGuildMember):
    __slots__ = ('user', 
                 'nick', 
                 'roles', 
                 'joined_at', 
                 'premium_since', 
                 'deaf', 
                 'mute', 
                 'pending', 
                 'permissions', 
                 'communication_disabled_until', 
                 'avatar_decoration_data')
    def __init__(self, **kwargs):
        '''
            Represents the Guild Member Structure defined here: https://discord.com/developers/docs/resources/guild#guild-member-object
        '''
        self.user = User(**kwargs.pop('user')) if 'user' in kwargs and kwargs['user'] is not None else None
        self.nick = kwargs.pop('nick', None)
        self.roles = kwargs.pop('roles', [])
        self.joined_at = kwargs.pop('joined_at', None)
        self.premium_since = kwargs.pop('premium_since', None)
        self.deaf = kwargs.pop('deaf', False)
        self.mute = kwargs.pop('mute', False)
        self.pending = kwargs.pop('pending', False)
        self.permissions = kwargs.pop('permissions', None)
        self.communication_disabled_until = kwargs.pop('communication_disabled_until', None)
        self.avatar_decoration_data = UserAvatarDecoration(**kwargs.pop('avatar_decoration_data')) if 'avatar_decoration_data' in kwargs and kwargs['avatar_decoration_data'] is not None else None

class GuildMemberAdd(GuildMember):
    __slots__ = ('guild_id')
    def __init__(self, **kwargs):
        '''
            Represents the Guild Member Add Structure defined here: https://discord.com/developers/docs/topics/gateway#guild-member-add
        '''
        super().__init__(**kwargs)
        self.guild_id = kwargs.pop('guild_id')

class GuildMemberRemove(BaseResourceObject):
    __slots__ = ('guild_id', 'user')
    def __init__(self, **kwargs):
        '''
            Represents the Guild Member Remove Structure defined here: https://discord.com/developers/docs/topics/gateway#guild-member-remove
        '''
        self.guild_id = kwargs.pop('guild_id')
        self.user = User(**kwargs.pop('user'))

class UserFlags(Enum):
    STAFF = 1
    PARTNER = 2
    HYPESQUAD = 4
    BUG_HUNTER_LEVEL_1 = 8
    HYPESQUAD_ONLINE_HOUSE_1 = 16
    HYPESQUAD_ONLINE_HOUSE_2 = 32
    HYPESQUAD_ONLINE_HOUSE_3 = 64
    PREMIUM_EARLY_SUPPORTER = 128
    TEAM_PSEUDO_USER = 256
    BUG_HUNTER_LEVEL_2 = 512
    VERIFIED_BOT = 1024
    VERIFIED_DEVELOPER = 2048
    CERTIFIED_MODERATOR = 4096
    BOT_HTTP_INTERACTIONS = 8192
    ACTIVE_DEVELOPER = 16384


