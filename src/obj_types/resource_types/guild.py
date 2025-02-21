from typing import List, Literal, Optional, TypedDict
from typing_extensions import NotRequired

from .snowflake import Snowflake, SnowflakeList
from .user import User, UserAvatarDecoration

DefaultMessageNotificationLevel = Literal[0, 1]
ExplicitContentFilterLevel = Literal[0, 1, 2]
MFALevel = Literal[0, 1]
VerificationLevel = Literal[0, 1, 2, 3, 4]
NSFWLevel = Literal[0, 1, 2, 3]
PremiumTier = Literal[0, 1, 2, 3]
GuildFeature = Literal[
    'ANIMATED_BANNER',
    'ANIMATED_ICON',
    'APPLICATION_COMMAND_PERMISSIONS_V2',
    'AUTO_MODERATION',
    'BANNER',
    'COMMUNITY',
    'CREATOR_MONETIZABLE_PROVISIONAL',
    'CREATOR_STORE_PAGE',
    'DEVELOPER_SUPPORT_SERVER',
    'DISCOVERABLE',
    'FEATURABLE',
    'INVITE_SPLASH',
    'INVITES_DISABLED',
    'MEMBER_VERIFICATION_GATE_ENABLED',
    'MONETIZATION_ENABLED',
    'MORE_EMOJI',
    'MORE_STICKERS',
    'NEWS',
    'PARTNERED',
    'PREVIEW_ENABLED',
    'ROLE_ICONS',
    'ROLE_SUBSCRIPTIONS_AVAILABLE_FOR_PURCHASE',
    'ROLE_SUBSCRIPTIONS_ENABLED',
    'TICKETED_EVENTS_ENABLED',
    'VANITY_URL',
    'VERIFIED',
    'VIP_REGIONS',
    'WELCOME_SCREEN_ENABLED',
    'RAID_ALERTS_DISABLED',
    'SOUNDBOARD',
    'MORE_SOUNDBOARD',
]

class PartialMember(TypedDict):
    roles: SnowflakeList
    joined_at: str
    deaf: bool
    mute: bool
    flags: int

class Ban(TypedDict):
    reason: Optional[str]
    user: User


class UnavailableGuild(TypedDict):
    id: Snowflake
    unavailable: NotRequired[bool]


class IncidentData(TypedDict):
    invites_disabled_until: NotRequired[Optional[str]]
    dms_disabled_until: NotRequired[Optional[str]]


class GuildMember(TypedDict):
    user: User
    nick: Optional[str]
    roles: List[Snowflake]
    joined_at: str
    premium_since: Optional[str]
    deaf: bool
    mute: bool
    pending: Optional[bool]
    permissions: Optional[str]
    communication_disabled_until: Optional[str]
    avatar_decoration_data: Optional[UserAvatarDecoration]