from typing import List, Literal, Optional, TypedDict, Union, Dict, Self
from typing_extensions import NotRequired

from .snowflake import Snowflake
from .user import User
from .guild import PartialMember
from .components import Component
from .poll import Poll
from .channel import Channel, ChannelMention, ChannelTag
from .sticker import StickerItem, Sticker
from .emoji import Emoji, PartialEmoji



class MessageAttachment(TypedDict):
    id: Snowflake
    filename: str
    title: Optional[str]
    description: Optional[str]
    content_type: Optional[str]
    size: int
    url: str
    proxy_url: str
    height: Optional[int]
    width: Optional[int]
    ephemeral: Optional[bool]
    duration_secs: Optional[int]
    waveforms: Optional[List[int]]
    flags: Optional[int]


class ReactionCountDetails(TypedDict):
    burst: int
    normal: int

class Reaction(TypedDict):
    count: int
    count_details: ReactionCountDetails
    me: bool
    me_burst: bool
    emoji: PartialEmoji
    burst_colors: List[str]

class MessageActivity(TypedDict):
    type: int
    party_id: Optional[str]



class MessageEmbedFooter(TypedDict):
    text: str
    icon_url: Optional[str]
    proxy_icon_url: Optional[str]

class MessageEmbedImage(TypedDict):
    url: str
    proxy_url: Optional[str]
    height: Optional[int]
    width: Optional[int]

class MessageEmbedThumbnail(TypedDict):
    url: str
    proxy_url: Optional[str]
    height: Optional[int]
    width: Optional[int]

class MessageEmbedVideo(TypedDict):
    url: str
    proxy_url: Optional[str]
    height: Optional[int]
    width: Optional[int]

class MessageEmbedProvider(TypedDict):
    name: Optional[str]
    url: Optional[str]

class MessageEmbedAuthor(TypedDict):
    name: str
    url: Optional[str]
    icon_url: Optional[str]
    proxy_icon_url: Optional[str]

class MessageEmbedField(TypedDict):
    name: str
    value: str
    inline: Optional[bool]

class MessageReference(TypedDict):
    type: Optional[int]
    message_id: Snowflake
    channel_id: Snowflake
    guild_id: Optional[Snowflake]
    fail_if_not_exists: Optional[bool]

class MessageInteractionMetadata(TypedDict):
    id : Snowflake
    type : int
    user: User
    authorizing_integration_owners: dict
    original_response_message_id: Snowflake
    interacted_message_id: Snowflake

class MessageInteraction(TypedDict):
    id: Snowflake
    type: int
    name: str
    user: User
    member: Optional[PartialMember]

class MessageRoleSubscription(TypedDict):
    role_subscription_listing_id: Snowflake
    tier_name: str
    total_months_subscribed: int
    is_renewal: bool

class MessageCall(TypedDict):
    participants: List[Snowflake]
    ended_timestamp: Optional[str]


class MessageEmbed(TypedDict):
    title: Optional[str]
    type: Optional[str]
    description: Optional[str]
    url: Optional[str]
    timestamp: Optional[str]
    color: Optional[int]
    footer: Optional[MessageEmbedFooter]
    image: Optional[MessageEmbedImage]
    thumbnail: Optional[MessageEmbedThumbnail]
    video: Optional[MessageEmbedVideo]
    provider: Optional[MessageEmbedProvider]
    fields: Optional[List[MessageEmbedField]]

class PartialMessage(TypedDict):
    type: int
    content: str
    embeds: List[MessageEmbed]
    attachments: List[dict]
    timestamp: str
    edited_timestamp: Optional[str]
    flags: int
    mentions: List[User]
    mention_roles: List[Snowflake]
    stickers: List[Sticker]
    sticker_items: List[StickerItem]
    components: List[Component]

class Message(TypedDict):
    id : Snowflake
    channel_id : Snowflake
    author : User
    content : str
    timestamp : str
    edited_timestamp : Optional[str]
    tts : bool
    mention_everyone : bool
    mentions : List[User]
    mention_roles : List[Snowflake]
    mention_channels : List[ChannelMention]
    attachments: List[MessageAttachment]
    embeds: List[MessageEmbed]
    reactions: List[Reaction]
    nonce: Optional[str]
    pinned: bool
    webhook_id: Optional[Snowflake]
    type: int
    activity: Optional[MessageActivity]
    application: Optional[Dict]
    application_id: Optional[Snowflake]
    flags: Optional[int]
    message_reference: Optional[MessageReference]
    message_snapshots: Optional[List[PartialMessage]]
    referenced_message: Optional[Self]
    interaction_metadata: Optional[MessageInteractionMetadata]
    interaction: Optional[MessageInteraction]
    thread: Optional[Channel]
    components: Optional[List[Component]]
    sticker_items: Optional[List[StickerItem]]
    stickers: Optional[List[Sticker]]
    position: Optional[int]
    role_subscription_data: Optional[MessageRoleSubscription]
    resolved: Optional[Dict]
    poll: Optional[Poll]
    call: Optional[MessageCall]