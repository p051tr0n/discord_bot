
from models.bot.resources.emoji import Emoji
from models.bot.resources.role import Role
from models.bot.events.presence import Presence
from models.bot.resources.channel import Channel
from models.bot.resources.stage import StageInstance
from models.bot.resources.audit import AuditLogEntry
from models.bot.resources.soundboard import SoundboardSound
from models.bot.resources.user import User, UserAvatarDecoration, GuildMember
from models.bot.resources.sticker import Sticker
from models.base import BaseResourceObject

__all__ = ['Guild', 
            'PartialGuild',
            'GuildPreview',
            'IncidentData',
            'WelcomeScreenChannel',
            'GuildCreate',
            'GuildAuditLogEntry',
            'GuildBan',
            'GuildEmojis',
            'GuildStickers',
            'GuildRole',
            'GuildRoleDelete',
            'GuildScheduledEvent',
            'GuildScheduledEventUser',
            'GuildSoundboardSoundDelete',
            'GuildSoundboardSounds']
            


class PartialGuild(BaseResourceObject):
    __slots__ = ('id', 'unavailable')
    def __init__(self, **kwargs):
        '''
            Represents the Partial Guild Structure defined here: https://discord.com/developers/docs/resources/guild#unavailable-guild-object
        '''
        super().__init__(**kwargs)
        self.id = kwargs.pop('id', '')
        self.unavailable = kwargs.pop('unavailable', False)

class IncidentData(BaseResourceObject):
    __slots__ = ('invites_disabled_until',
                    'dms_disabled_until',
                    'dm_spam_detected_at',
                    'raid_detected_at')
    def __init__(self, **kwargs):
        self.invites_disabled_until = kwargs.pop('invites_disabled_until')
        self.dms_disabled_until = kwargs.pop('dms_disabled_until')
        self.dm_spam_detected_at = kwargs.pop('dm_spam_detected_at', None)
        self.raid_detected_at = kwargs.pop('raid_detected_at', None)

class WelcomeScreenChannel(BaseResourceObject):
    __slots__ = ('channel_id', 'description', 'emoji_id', 'emoji_name')
    def __init__(self, **kwargs):
        '''
            Represents the Welcome Screen Channel Structure defined here: https://discord.com/developers/docs/resources/guild#welcome-screen-channel-object
        '''
        self.channel_id = kwargs.pop('channel_id')
        self.description = kwargs.pop('description')
        self.emoji_id = kwargs.pop('emoji_id')
        self.emoji_name = kwargs.pop('emoji_name', None)





class GuildPreview(BaseResourceObject):
    __slots__ = ('id',
                    'name',
                    'icon',
                    'splash',
                    'discovery_splash',
                    'emojis',
                    'features',
                    'approximate_member_count',
                    'approximate_presence_count',
                    'description',
                    'stickers')
    def __init__(self, **kwargs):
        '''
            Represents the Guild Preview Structure defined here: https://discord.com/developers/docs/resources/guild#guild-preview-object
        '''
        self.id                         = kwargs.get('id')
        self.name                       = kwargs.get('name')
        self.icon                       = kwargs.get('icon')
        self.splash                     = kwargs.get('splash')
        self.discovery_splash           = kwargs.get('discovery_splash')
        self.emojis                     = [Emoji(**x) for x in kwargs.get('emojis')]
        self.features                   = kwargs.get('features')
        self.approximate_member_count   = kwargs.get('approximate_member_count')
        self.approximate_presence_count = kwargs.get('approximate_presence_count')
        self.description                = kwargs.get('description')
        self.stickers                   = [Sticker(**x) for x in kwargs.get('stickers')]

class Guild(GuildPreview):
    __slots__ = ('owner',
                    'owner_id',
                    'permissions',
                    'region',
                    'afk_channel_id',
                    'afk_timeout',
                    'widget_enabled',
                    'widget_channel_id',
                    'verification_level',
                    'default_message_notifications',
                    'explicit_content_filter',
                    'roles',
                    'emojis',
                    'features',
                    'mfa_level',
                    'application_id',
                    'system_channel_id',
                    'system_channel_flags',
                    'rules_channel_id',
                    'max_presences',
                    'max_members',
                    'vanity_url_code',
                    'description',
                    'banner',
                    'premium_tier',
                    'premium_subscription_count',
                    'preferred_locale',
                    'public_updates_channel_id',
                    'max_video_channel_users',
                    'max_stage_video_channel_users',
                    'approximate_member_count',
                    'approximate_presence_count',
                    'welcome_screen',
                    'nsfw_level',
                    'stickers',
                    'premium_progress_bar_enabled',
                    'safety_alerts_channel_id',
                    'incidents_data')
    def __init__(self, **kwargs):
        '''
            Represents the Guild Structure defined here: https://discord.com/developers/docs/resources/guild#guild-object
        '''
        super().__init__(**kwargs)
        self.owner                          = User(**kwargs.get('owner')) if 'owner' in kwargs else None
        self.owner_id                       = kwargs.get('owner_id')
        self.permissions                    = kwargs.get('permissions')
        self.region                         = kwargs.get('region')
        self.afk_channel_id                 = kwargs.get('afk_channel_id', None)
        self.afk_timeout                    = kwargs.get('afk_timeout')
        self.widget_enabled                 = kwargs.get('widget_enabled', None)
        self.widget_channel_id              = kwargs.get('widget_channel_id', None)
        self.verification_level             = kwargs.get('verification_level')
        self.default_message_notifications  = kwargs.get('default_message_notifications')
        self.explicit_content_filter        = kwargs.get('explicit_content_filter')
        self.roles                          = [Role(**x) for x in kwargs.get('roles')]
        self.emojis                         = [Emoji(**x) for x in kwargs.get('emojis')]
        self.features                       = kwargs.get('features')
        self.mfa_level                      = kwargs.get('mfa_level')
        self.application_id                 = kwargs.get('application_id')
        self.system_channel_id              = kwargs.get('system_channel_id')
        self.system_channel_flags           = kwargs.get('system_channel_flags')
        self.rules_channel_id               = kwargs.get('rules_channel_id')
        self.max_presences                  = kwargs.get('max_presences', None)
        self.max_members                    = kwargs.get('max_members', None)
        self.vanity_url_code                = kwargs.get('vanity_url_code')
        self.description                    = kwargs.get('description')
        self.banner                         = kwargs.get('banner')
        self.premium_tier                   = kwargs.get('premium_tier')
        self.premium_subscription_count     = kwargs.get('premium_subscription_count', None)
        self.preferred_locale               = kwargs.get('preferred_locale')
        self.public_updates_channel_id      = kwargs.get('public_updates_channel_id')
        self.max_video_channel_users        = kwargs.get('max_video_channel_users', None)
        self.max_stage_video_channel_users  = kwargs.get('max_stage_video_channel_users', None)
        self.approximate_member_count       = kwargs.get('approximate_member_count', None)
        self.approximate_presence_count     = kwargs.get('approximate_presence_count', None)
        self.welcome_screen                 = WelcomeScreenChannel(**kwargs.get('welcome_screen')) if 'welcome_screen' in kwargs else None
        self.nsfw_level                     = kwargs.get('nsfw_level')
        self.stickers                       = [Sticker(**x) for x in kwargs.get('stickers')] if 'stickers' in kwargs else None
        self.premium_progress_bar_enabled   = kwargs.get('premium_progress_bar_enabled', False)
        self.safety_alerts_channel_id       = kwargs.get('safety_alerts_channel_id', None)
        self.incidents_data                 = IncidentData(**kwargs.get('incidents_data')) if 'incidents_data' in kwargs and kwargs['incidents_data'] is not None else None

class GuildCreate(Guild):
    __slots__ = (
                    'joined_at',
                    'large',
                    'unavailable',
                    'member_count',
                    'voice_states',
                    'members',
                    'channels',
                    'threads',
                    'presences',
                    'stage_instances',
                    'guild_scheduled_events',
                    'soundboard_sounds'
    )

    def __init__(self, **kwargs):
        '''
            Represents the Guild Create Structure defined here: https://discord.com/developers/docs/topics/gateway#guild-create
        '''
        super().__init__(**kwargs)
        self.joined_at              = kwargs.get('joined_at')
        self.large                  = kwargs.get('large')
        self.unavailable            = kwargs.get('unavailable', None)
        self.member_count           = kwargs.get('member_count')
        self.voice_states           = [VoiceState(**x) for x in kwargs.get('voice_states')]
        self.members                = [GuildMember(**x) for x in kwargs.get('members')]
        self.channels               = [Channel(**x) for x in kwargs.get('channels')]
        self.threads                = [Channel(**x) for x in kwargs.get('threads')]
        self.presences              = [Presence(**x) for x in kwargs.get('presences')]
        self.stage_instances        = [StageInstance(**x) for x in kwargs.get('stage_instances')]
        self.guild_scheduled_events = [GuildScheduledEvent(**x) for x in kwargs.get('guild_scheduled_events')]
        self.soundboard_sounds      = [SoundboardSound(**x) for x in kwargs.get('soundboard_sounds')]

class GuildAuditLogEntry(AuditLogEntry):
    __slots__ = ('guild_id')
    def __init__(self, **kwargs):
        '''
            Represents the Guild Audit Log Entry Create Structure defined here: https://discord.com/developers/docs/resources/audit-log#audit-log-entry-object-audit-log-events
        '''
        super().__init__(**kwargs)
        self.guild_id = kwargs.get('guild_id')

class GuildBan(BaseResourceObject):
    __slots__ = ('guild_id', 'user')
    def __init__(self, **kwargs):
        self.guild_id = kwargs.get('guild_id')
        self.user = User(**kwargs.get('user'))

class GuildEmojis(BaseResourceObject):
    __slots__ = ('guild_id', 'emojis')
    def __init__(self, **kwargs):
        self.guild_id = kwargs.get('guild_id')
        self.emojis = [Emoji(**x) for x in kwargs.get('emojis')] if 'emojis' in kwargs else []

class GuildStickers(BaseResourceObject):
    __slots__ = ('guild_id', 'stickers')
    def __init__(self, **kwargs):
        self.guild_id = kwargs.get('guild_id')
        self.stickers = [Sticker(**x) for x in kwargs.get('stickers')] if 'stickers' in kwargs else []

class GuildRole(BaseResourceObject):
    __slots__ = ('guild_id', 'role')
    def __init__(self, **kwargs):
        self.guild_id = kwargs.get('guild_id')
        self.role = Role(**kwargs.get('role'))

class GuildRoleDelete(BaseResourceObject):
    __slots__ = ('guild_id', 'role_id')
    def __init__(self, **kwargs):
        self.guild_id = kwargs.get('guild_id')
        self.role_id = kwargs.get('role_id')

class GuildScheduledEvent(BaseResourceObject):
    __slots__ = (
                    'id',
                    'guild_id',
                    'channel_id',
                    'creator_id',
                    'name',
                    'description',
                    'scheduled_start_time',
                    'scheduled_end_time',
                    'privacy_level',
                    'status',
                    'entity_type',
                    'entity_id',
                    'entity_metadata',
                    'creator',
                    'user_count',
                    'image',
                    'recurrence_rule'
                )
    def __init__(self, **kwargs):
        self.id                     = kwargs.get('id')
        self.guild_id               = kwargs.get('guild_id')
        self.channel_id             = kwargs.get('channel_id')
        self.creator_id             = kwargs.get('creator_id', None)
        self.name                   = kwargs.get('name')
        self.description            = kwargs.get('description', None)
        self.scheduled_start_time   = kwargs.get('scheduled_start_time')
        self.scheduled_end_time     = kwargs.get('scheduled_end_time')
        self.privacy_level          = kwargs.get('privacy_level')
        self.status                 = kwargs.get('status')
        self.entity_type            = kwargs.get('entity_type')
        self.entity_id              = kwargs.get('entity_id')
        self.entity_metadata        = kwargs.get('entity_metadata')
        self.creator                = User(**kwargs.get('creator')) if 'creator' in kwargs else None
        self.user_count             = kwargs.get('user_count', None)
        self.image                  = kwargs.get('image', None)
        self.recurrence_rule        = kwargs.get('recurrence_rule')

class GuildScheduledEventUser(BaseResourceObject):
    __slots__ = ('id', 'user_id', 'scheduled_event_id')
    def __init__(self, **kwargs):
        self.id                 = kwargs.get('id')
        self.user_id            = kwargs.get('user_id')
        self.scheduled_event_id = kwargs.get('scheduled_event_id')

class GuildSoundboardSoundDelete(BaseResourceObject):
    __slots__ = ('guild_id', 'sound_id')
    def __init__(self, **kwargs):
        self.guild_id = kwargs.get('guild_id')
        self.sound_id = kwargs.get('sound_id')

class GuildSoundboardSounds(BaseResourceObject):
    __slots__ = ('guild_id', 'soundboard_sounds')
    def __init__(self, **kwargs):
        self.guild_id = kwargs.get('guild_id')
        self.sound_id = [SoundboardSound(**x) for x in kwargs.get('soundboard_sounds')]