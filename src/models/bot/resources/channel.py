from typing import List
from typing_extensions import Optional

from models.bot.resources.user import User, GuildMember
from models.base import BaseResourceObject
from obj_types.resource_types.snowflake import Snowflake


__all__ = ['Channel', 
            'ChannelMention', 
            'Overwrite', 
            'ThreadMetadata', 
            'ThreadMember', 
            'ChannelTag', 
            'DefaultReaction',
            'ChannelPinsUpdate',
            'ThreadListSync',
            'ThreadMembersUpdate']
            

class Channel(BaseResourceObject):
    __slots__ = ('id',
                 'type', 
                 'guild_id', 
                 'position', 
                 'permission_overwrites', 
                 'name', 
                 'topic', 
                 'nsfw', 
                 'last_message_id', 
                 'bitrate',
                 'user_limit', 
                 'rate_limit_per_user', 
                 'recipients', 
                 'icon', 
                 'owner_id', 
                 'application_id', 
                 'managed', 
                 'parent_id', 
                 'last_pin_timestamp', 
                 'rtc_region', 
                 'video_quality_mode', 
                 'message_count', 
                 'member_count', 
                 'thread_metadata', 
                 'member', 
                 'default_auto_archive_duration', 
                 'permissions', 
                 'flags', 
                 'total_message_sent', 
                 'available_tags', 
                 'applied_tags', 
                 'default_reaction_emoji',
                 'default_thread_rate_limit_per_user', 
                 'default_sort_order',
                 'default_forum_layout')

    def __init__(self, **kwargs):
        self.id: Snowflake                                      = kwargs.get('id', "")
        self.type: int                                          = kwargs.get('type', 0)
        self.guild_id: Optional[Snowflake]                      = kwargs.get('guild_id', None)
        self.position: Optional[int]                            = kwargs.get('position', None)
        self.permission_overwrites: Optional[List[Overwrite]]   = [Overwrite(**x) for x in kwargs.get('permission_overwrites')] if 'permission_overwrites' in kwargs else None
        self.name: Optional[str]                                = kwargs.get('name', None)
        self.topic: Optional[str]                               = kwargs.get('topic', None)
        self.nsfw: Optional[bool]                               = kwargs.get('nsfw', None)
        self.last_message_id: Optional[Snowflake]               = kwargs.get('last_message_id', None)
        self.bitrate: Optional[int]                             = kwargs.get('bitrate', None)
        self.user_limit: Optional[int]                          = kwargs.get('user_limit', None)
        self.rate_limit_per_user: Optional[int]                 = kwargs.get('rate_limit_per_user', None)
        self.recipients: Optional[List[User]]                   = [User(**x) for x in kwargs.get('recipients')] if 'recipients' in kwargs else None
        self.icon: Optional[str]                                = kwargs.get('icon', None)
        self.owner_id: Optional[Snowflake]                      = kwargs.get('owner_id', None)
        self.application_id: Optional[Snowflake]                = kwargs.get('application_id', None)
        self.managed: Optional[bool]                            = kwargs.get('managed', None)
        self.parent_id: Optional[Snowflake]                     = kwargs.get('parent_id', "")
        self.last_pin_timestamp: Optional[str]                  = kwargs.get('last_pin_timestamp', None)
        self.rtc_region: Optional[str]                          = kwargs.get('rtc_region', None)
        self.video_quality_mode: Optional[int]                  = kwargs.get('video_quality_mode', None)
        self.message_count: Optional[int]                       = kwargs.get('message_count', None)
        self.member_count: Optional[int]                        = kwargs.get('member_count', None)
        self.thread_metadata: Optional[ThreadMetadata]          = ThreadMetadata(**kwargs.get('thread_metadata')) if 'thread_metadata' in kwargs else None
        self.member: Optional[ThreadMember]                     = ThreadMember(**kwargs.get('member')) if 'member' in kwargs else None
        self.default_auto_archive_duration: Optional[int]       = kwargs.get('default_auto_archive_duration', None)
        self.permissions: Optional[str]                         = kwargs.get('permissions', None)
        self.flags: Optional[int]                               = kwargs.get('flags', None)
        self.total_message_sent: Optional[int]                  = kwargs.get('total_message_sent', None)
        self.available_tags: Optional[List[ChannelTag]]         = [ChannelTag(**x) for x in kwargs.get('available_tags')] if 'available_tags' in kwargs else None
        self.applied_tags: Optional[List[Snowflake]]            = kwargs.get('applied_tags', None)
        self.default_reaction_emoji: Optional[DefaultReaction]  = DefaultReaction(**kwargs.get('default_reaction_emoji')) if 'default_reaction_emoji' in kwargs else None
        self.default_thread_rate_limit_per_user: Optional[int]  = kwargs.get('default_thread_rate_limit_per_user', None)
        self.default_sort_order: Optional[int]                  = kwargs.get('default_sort_order', None)
        self.default_forum_layout: Optional[int]                = kwargs.get('default_forum_layout', None)


class DefaultReaction(BaseResourceObject):
    __slots__ = ('emoji_id', 'emoji_name')
    def __init__(self, **kwargs):
        self.emoji_id   = kwargs.get('emoji_id')
        self.emoji_name = kwargs.get('emoji_name')

class ChannelTag(BaseResourceObject):
    __slots__ = ('id', 'name', 'moderated', 'emoji_id', 'emoji_name')
    def __init__(self, **kwargs):
        self.id         = kwargs.get('id')
        self.name       = kwargs.get('name')
        self.moderated  = kwargs.get('moderated')
        self.emoji_id   = kwargs.get('emoji_id')
        self.emoji_name = kwargs.get('emoji_name')

class ChannelMention(BaseResourceObject):
    __slots__ = ('id', 'guild_id', 'type', 'name')
    def __init__(self, **kwargs):
        self.id         = kwargs.get('id', "")
        self.guild_id   = kwargs.get('guild_id', "")
        self.type       = kwargs.get('type', 0)
        self.name       = kwargs.get('name', "")

class ChannelPinsUpdate(BaseResourceObject):
    __slots__ = ('guild_id', 'channel_id', 'last_pin_timestamp')
    def __init__(self, **kwargs):
        self.guild_id           = kwargs.get('guild_id', None)
        self.channel_id         = kwargs.get('channel_id')
        self.last_pin_timestamp = kwargs.get('last_pin_timestamp', "")

class Overwrite(BaseResourceObject):
    __slots__ = ('id', 'type', 'allow', 'deny')
    def __init__(self, **kwargs):
        self.id         = kwargs.get('id', "")
        self.type       = kwargs.get('type', 0)
        self.allow      = kwargs.get('allow', 0)
        self.deny       = kwargs.get('deny', 0)

class ThreadListSync(BaseResourceObject):
    __slots__ = ('guild_id', 'channel_ids', 'threads', 'members')
    def __init__(self, **kwargs):
        self.guild_id       = kwargs.get('guild_id')
        self.channel_ids    = [x for x in kwargs.get('channel_ids')] if 'channel_ids' in kwargs else None
        self.threads        = [Channel(**x) for x in kwargs.get('threads')]
        self.members        = [ThreadMember(**x) for x in kwargs.get('members')]

class ThreadMetadata(BaseResourceObject):
    __slots__ = ('archive_timestamp', 'archived', 'auto_archive_duration', 'locked', 'invitable', 'create_timestamp')
    def __init__(self, **kwargs):
        self.archive_timestamp      = kwargs.get('archive_timestamp')
        self.archived               = kwargs.get('archived')
        self.auto_archive_duration  = kwargs.get('auto_archive_duration')
        self.locked                 = kwargs.get('locked')
        self.invitable              = kwargs.get('invitable', None)
        self.create_timestamp       = kwargs.get('create_timestamp', None)

class ThreadMember(BaseResourceObject):
    __slots__ = ('id', 'user_id', 'join_timestamp', 'flags', 'member')
    def __init__(self, **kwargs):
        self.id             = kwargs.get('id', None)
        self.user_id        = kwargs.get('user_id', None)
        self.join_timestamp = kwargs.get('join_timestamp')
        self.flags          = kwargs.get('flags')
        self.member         = GuildMember(**kwargs.get('member')) if 'member' in kwargs else None

class ThreadMembersUpdate(BaseResourceObject):
    __slots__ = ('id', 'guild_id', 'member_count', 'added_members', 'removed_member_ids')

    def __init__(self, **kwargs):
        self.id                 = kwargs.get('id')
        self.guild_id           = kwargs.get('guild_id')
        self.member_count       = kwargs.get('member_count')
        self.added_members      = [ThreadMember(**x) for x in kwargs.get('added_members')] if 'added_members' in kwargs else None
        self.removed_member_ids = [x for x in kwargs.get('removed_member_ids')] if 'removed_member_ids' in kwargs else None