from typing import List, Literal, Optional, TypedDict, Union
from typing_extensions import NotRequired

from .user import PartialUser
from .snowflake import Snowflake
from .guild import GuildMember

class Overwrite(TypedDict):
    id: Snowflake
    type: int
    allow: str
    deny: str

class ThreadMetadata(TypedDict):
    archived: bool
    auto_archive_duration: int
    archive_timestamp: str
    locked: bool
    invitable: Optional[bool]
    create_timestamp: str

class ThreadMember(TypedDict):
    id: Snowflake
    user_id: Snowflake
    join_timestamp: str
    flags: int
    member: GuildMember

class ChannelMention(TypedDict):
    id: Snowflake
    guild_id: Snowflake
    type: int
    name: str

class ChannelTag(TypedDict):
    id: Snowflake
    name: str
    moderated: bool
    emoji_id: Snowflake
    emoji_name: str

class DefaultReaction(TypedDict):
    emoji_id: Snowflake
    emoji_name: str

class Channel(TypedDict):
    id: Snowflake
    type: int
    guild_id: Optional[Snowflake]
    position: Optional[int]
    permission_overwrites: List[Overwrite]
    name: Optional[str]
    topic: Optional[str]
    nsfw: Optional[bool]
    last_message_id: Optional[Snowflake]
    bitrate: Optional[int]
    user_limit: Optional[int]
    rate_limit_per_user: Optional[int]
    recipients: Optional[List[PartialUser]]
    icon: Optional[str]
    owner_id: Optional[Snowflake]
    application_id: Optional[Snowflake]
    managed: Optional[bool]
    parent_id: Optional[str]
    last_pin_timestamp: Optional[str]
    rtc_region: Optional[str]
    message_count: Optional[int]
    member_count: Optional[int]
    thread_metadata: Optional[ThreadMetadata]
    thread_member: Optional[ThreadMember]
    default_auto_archive_duration: Optional[int]
    permissions: Optional[str]
    flags: Optional[int]
    total_message_sent: Optional[int]
    available_tags: Optional[List[ChannelTag]]
    applied_tags: Optional[List[str]]
    default_reaction_emoji: Optional[DefaultReaction]
    default_thread_rate_limit_per_user: Optional[int]
    default_sort_order: Optional[int]
    default_forum_layout: Optional[int]
