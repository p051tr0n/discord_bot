from typing import (
    Dict,
    List,
    Optional,
    Union,
    Any,
    Tuple,
    TypedDict,
    TYPE_CHECKING,
    Literal
)
from typing_extensions import NotRequired
import datetime

from src.models.bot.resources.emoji import Emoji

from src.models.bot.resources.role import Role

from src.models.bot.resources.user import User, PartialGuildMember, GuildMember
from src.models.bot.resources.channel import Channel
from src.models.bot.resources.application import PartialApplication
from src.models.base import BaseResourceObject

from src.obj_types.resource_types.message import (
    Message,
    PartialMessage,
    MessageEmbed,
    MessageAttachment,
    MessageEmbedFooter,
    MessageEmbedImage,
    MessageEmbedThumbnail,
    MessageEmbedVideo,
    MessageEmbedProvider,
    MessageEmbedAuthor,
    MessageEmbedField,
    Reaction,
    ReactionCountDetails,
    MessageActivity,
    MessageReference,
    MessageCall,
    MessageInteractionMetadata,
    MessageInteraction,
    MessageRoleSubscription,
)

from src.obj_types.resource_types.user import User
from src.obj_types.resource_types.snowflake import Snowflake
from src.obj_types.resource_types.guild import PartialMember
from src.obj_types.resource_types.components import Component
from src.obj_types.resource_types.poll import Poll
from src.obj_types.resource_types.channel import Channel, ChannelMention, ChannelTag
from src.obj_types.resource_types.sticker import StickerItem, Sticker
from src.obj_types.resource_types.emoji import Emoji, PartialEmoji
from src.obj_types.resource_types.role import Role
from src.obj_types.resource_types.components import Component

__all__ = ['PartialMessage', 
            'Message', 
            'MessageCreate', 
            'MessageUpdate', 
            'ChannelMention', 
            'MessageAttachment', 
            'MessageEmbed', 
            'MessageEmbedLimitError', 
            'MessageEmbedFooter', 
            'MessageEmbedImage', 
            'MessageEmbedThumbnail', 
            'MessageEmbedVideo', 
            'MessageEmbedProvider', 
            'MessageEmbedAuthor', 
            'MessageEmbedField', 
            'Reaction', 
            'ReactionCountDetails', 
            'MessageActivity', 
            'MessageReference', 
            'MessageSnapshot', 
            'MessageStickerItem', 
            'MessageRoleSubscription', 
            'MessageResolved',
            'MessageReactionRemove',
            'MessageReactionAdd',
            'MessageReactionRemoveAll',
            'MessageReactionRemoveEmoji']

#-----------------------------------------------------------------------------------------------------------------
class PartialMessage(BaseResourceObject):

    __slots__ = (
        'type',
        'content',
        'embeds',
        'attachments',
        'timestamp',
        'edited_timestamp',
        'flags',
        'mentions',
        'mention_roles',
        'sitckers',
        'sticker_items',
        'components'
    )

    def __init__(self, **kwargs):
        self.type: int                              = kwargs.get('type', 0)
        self.content: str                           = kwargs.get('content', "")
        self.embeds: List[MessageEmbed]             = [MessageEmbed(**x) for x in kwargs.get('embeds')] if 'embeds' in kwargs and kwargs['embeds'] is not None else list()
        self.attachments: List[MessageAttachment]   = [MessageAttachment(**x) for x in kwargs.get('attachments')] if 'attachments' in kwargs and kwargs['attachments'] is not None else list()
        self.timestamp: str                         = kwargs.get('timestamp', "")
        self.edited_timestamp: Optional[str]        = kwargs.get('edited_timestamp', "")
        self.flags: int                             = kwargs.get('flags', 0)
        self.mentions: List[User]                   = [User(**x) for x in kwargs.get('mentions')] if 'mentions' in kwargs and kwargs['mentions'] is not None else list()
        self.mention_roles: List[Role]              = [Role(**x) for x in kwargs.get('mention_roles')] if 'mention_roles' in kwargs and kwargs['mention_roles'] is not None else list()
        self.sitckers: List[Sticker]                = kwargs.get('stickers', None)
        self.sticker_items: List[StickerItem]       = kwargs.get('sticker_items', None)
        self.components: List[Component]            = kwargs.get('components', None)

#-----------------------------------------------------------------------------------------------------------------
class Message(BaseResourceObject):

    __slots__ = (
        'id',
        'channel_id',
        'author',
        'content',
        'timestamp',
        'edited_timestamp',
        'tts',
        'mention_everyone',
        'mentions',
        'mention_roles',
        'mention_channels',
        'attachments',
        'embeds',
        'reactions',
        'nonce',
        'pinned',
        'webhook_id',
        'type',
        'activity',
        'application',
        'application_id',
        'flags',
        'message_reference',
        'message_snapshots',
        'referenced_messages',
        'interaction_metadata',
        'interaction',
        'thread',
        'components',
        'sticker_items',
        'sticker',
        'position',
        'role_subscription_data',
        'resolved',
        'poll',
        'call'
    )

    def __init__(self, **kwargs):
        self.id: Snowflake =                                                kwargs.get('id', "")
        self.channel_id: Snowflake =                                        kwargs.get('channel_id', "")
        self.author: User =                                                 User(**kwargs.get('author', {}))
        self.content: str =                                                 kwargs.get('content', "")
        self.timestamp: str =                                               kwargs.get('timestamp', "")
        self.edited_timestamp: Optional[str] =                              kwargs.get('edited_timestamp', "")
        self.tts: bool =                                                    kwargs.get('tts', False)
        self.mention_everyone: bool =                                       kwargs.get('mention_everyone', False)
        self.mentions: List[User] =                                         [User(**x) for x in kwargs.get('mentions')] if 'mentions' in kwargs and kwargs['mentions'] is not None else list()
        self.mention_roles: List[Snowflake] =                               kwargs.get('mention_roles', list())
        self.mention_channels: List[ChannelMention] =                       [ChannelMention(**x) for x in kwargs.get('mention_channels')] if 'mention_channels' in kwargs and kwargs['mention_channels'] is not None else None
        self.attachments: List[MessageAttachment] =                         [MessageAttachment(**x) for x in kwargs.get('attachments')] if 'attachments' in kwargs and kwargs['attachments'] is not None else list()
        self.embeds: List[MessageEmbed] =                                   [MessageEmbed(**x) for x in kwargs.get('embeds')] if 'embeds' in kwargs and kwargs['embeds'] is not None else list()
        self.reactions: List[Reaction] =                                    [Reaction(**x) for x in kwargs.get('reactions')] if 'reactions' in kwargs and kwargs['reactions'] is not None else None
        self.nonce: Optional[str] =                                         kwargs.get('nonce', None)
        self.pinned: bool =                                                 kwargs.get('pinned', False)
        self.webhook_id: Optional[Snowflake] =                              kwargs.get('webhook_id', None)
        self.type: int =                                                    kwargs.get('type', 0)
        self.activity: Optional[MessageActivity] =                          MessageActivity(**kwargs.get('activity')) if 'activity' in kwargs and kwargs['activity'] is not None else None
        self.application: Optional[Dict] =                                  PartialApplication(**kwargs.get('application')) if 'application' in kwargs and kwargs['application'] is not None else None
        self.application_id: Optional[Snowflake] =                          kwargs.get('application_id', None)
        self.flags: Optional[int] =                                         kwargs.get('flags', None)
        self.message_reference: Optional[MessageReference] =                MessageReference(**kwargs.get('message_reference')) if 'message_reference' in kwargs and kwargs['message_reference'] is not None else None
        self.message_snapshots: Optional[List[PartialMessage]] =            kwargs.get('message_snapshots', None)
        self.referenced_messages: Optional[Message] =                       Message(**kwargs.pop('referenced_messages')) if 'referenced_messages' in kwargs and kwargs['referenced_messages'] is not None else False
        self.interaction_metadata: Optional[MessageInteractionMetadata] =   kwargs.get('interaction_metadata', None)
        self.interaction: Optional[MessageInteraction] =                    kwargs.get('interaction', None)
        self.thread: Optional[Channel] =                                    Channel(**kwargs.get('thread')) if 'thread' in kwargs and kwargs['thread'] is not None else None
        self.components: Optional[List[Component]] =                        kwargs.get('components', None)
        self.sticker_items: Optional[List[StickerItem]] =                   [MessageStickerItem(**x) for x in kwargs.get('sticker_items')] if 'sticker_items' in kwargs and kwargs['sticker_items'] is not None else None
        self.sticker: Optional[List[Sticker]] =                             kwargs.get('sticker', None)
        self.position: Optional[int] =                                      kwargs.get('position', None)
        self.role_subscription_data: Optional[MessageRoleSubscription] =    MessageRoleSubscription(**kwargs.get('role_subscription_data')) if 'role_subscription_data' in kwargs and kwargs['role_subscription_data'] is not None else None
        self.resolved: Optional[Dict] =                                     kwargs.get('resolved', None)
        self.poll: Optional[Poll] =                                         kwargs.get('poll', None)
        self.call: Optional[MessageCall] =                                  kwargs.get('call', None)

#-----------------------------------------------------------------------------------------------------------------
class MessageCreate(Message):
    __slots__ = ('guild_id', 'member', 'mentions')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.guild_id: Snowflake    = kwargs.get('guild_id', None)
        self.member: PartialMember  = PartialGuildMember(**kwargs.get('member')) if 'member' in kwargs and kwargs['member'] is not None else None
        self.mentions: List[User]   = [User(**x) for x in kwargs.get('mentions')] if 'mentions' in kwargs and kwargs['mentions'] is not None else list()

#-----------------------------------------------------------------------------------------------------------------
class MessageUpdate(MessageCreate):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

#-----------------------------------------------------------------------------------------------------------------
class ChannelMention(BaseResourceObject):
    __slots__ = ('id', 'guild_id', 'type', 'name')

    def __init__(self, **kwargs):
        self.id: Snowflake =        kwargs.get('id', "")
        self.guild_id: Snowflake =  kwargs.get('guild_id', "")
        self.type: int =            kwargs.get('type', 0)
        self.name: str =            kwargs.get('name', "")

#-----------------------------------------------------------------------------------------------------------------
class MessageAttachment(BaseResourceObject):

    __slots__ = (
        'id',
        'filename',
        'title',
        'description',
        'content_type',
        'size',
        'url',
        'proxy_url',
        'height',
        'width',
        'ephemeral',
        'duration_secs',
        'waveform',
        'flags'
    )


    def __init__(self, **kwargs):
        self.id: Snowflake =                kwargs.get('id', "")
        self.filename: str =                kwargs.get('filename', "")
        self.title: Optional[str] =         kwargs.get('title', None)
        self.description: Optional[str] =   kwargs.get('description', None)
        self.content_type =                 kwargs.get('content_type', None)
        self.size =                         kwargs.get('size', 0)
        self.url =                          kwargs.get('url', "")
        self.proxy_url =                    kwargs.get('proxy_url', "")
        self.height =                       kwargs.get('height', None)
        self.width =                        kwargs.get('width', None)
        self.ephemeral =                    kwargs.get('ephemeral', False)
        self.duration_secs =                kwargs.get('duration_secs', None)
        self.waveform =                     kwargs.get('waveform', None)
        self.flags =                        kwargs.get('flags', None)

#-----------------------------------------------------------------------------------------------------------------
class MessageEmbedLimitError(Exception):
    def __init__(self, message, errors):
        super().__init__(message)
        self.errors = errors

#-----------------------------------------------------------------------------------------------------------------
class MessageEmbed(BaseResourceObject):

    __slots__ = (
        'title',
        'type',
        'description',
        'url',
        'timestamp',
        'color',
        'footer',
        'image',
        'thumbnail',
        'video',
        'provider',
        'author',
        'fields'
    )
    def __init__(self, **kwargs):
        self.title: Optional[str] =                         kwargs.get('title', None)
        self.type: Optional[str] =                          kwargs.get('type', None)
        self.description: Optional[str] =                   kwargs.get('description', None)
        self.url: Optional[str] =                           kwargs.get('url', None)
        self.timestamp: Optional[str] =                     kwargs.get('timestamp', None)
        self.color: Optional[int] =                         kwargs.get('color', None)
        self.footer:Optional[MessageEmbedFooter] =          MessageEmbedFooter(**kwargs.get('footer')) if 'footer' in kwargs and kwargs['footer'] is not None else None
        self.image: Optional[MessageEmbedImage] =           MessageEmbedImage(**kwargs.get('image')) if 'image' in kwargs and kwargs['image'] is not None else None
        self.thumbnail: Optional[MessageEmbedThumbnail]  =  MessageEmbedThumbnail(**kwargs.get('thumbnail')) if 'thumbnail' in kwargs and kwargs['thumbnail'] is not None else None
        self.video: Optional[MessageEmbedVideo] =           MessageEmbedVideo(**kwargs.get('video')) if 'video' in kwargs and kwargs['video'] is not None else None
        self.provider: Optional[MessageEmbedProvider] =     MessageEmbedProvider(**kwargs.get('provider')) if 'provider' in kwargs and kwargs['provider'] is not None else None
        self.author: Optional[MessageEmbedAuthor] =         MessageEmbedAuthor(**kwargs.get('author')) if 'author' in kwargs and kwargs['author'] is not None else None
        self.fields: Optional[List[MessageEmbedField]] =    [MessageEmbedField(**x) for x in kwargs.get('fields')] if 'fields' in kwargs and kwargs['fields'] is not None else None

        self.check_embed_limits()

    #all of the variables checked in this function should be made into properties so that the checking is done
    #when the value is set, rather than when the object is created.
    def check_embed_limits(self):
        errors = dict()

        if self.title is not None and len(self.title) > 256:
            errors['title'] = f'Title length is {len(self.title)}, maximum is 256.'
        if self.description is not None and len(self.description) > 4096:
            errors['description'] = f'Description length is {len(self.description)}, maximum is 4096.'
        if self.fields is not None and len(self.fields) > 25:
            errors['fields'] = f'Fields length is {len(self.fields)}, maximum is 25.'
        if self.fields is not None and not isinstance(self.fields, list):
            errors['fields'] = f'Fields must be a list.'

        if self.fields is not None:
            for x in range(len(self.fields)):
                if len(self.fields[x].name) > 256:
                    errors[f'fields[{x}].name'] = f'Field name length is {len(self.fields[x].name)}, maximum is 256.'
                if len(self.fields[x].value) > 1024:
                    errors[f'fields[{x}].value'] = f'Field value length is {len(self.fields[x].value)}, maximum is 1024.'

        if isinstance(self.footer, MessageEmbedFooter) and len(self.footer.text) > 2048:
            errors['footer.text'] = f'Footer text length is {len(self.footer.text)}, maximum is 2048.'

        if isinstance(self.author, MessageEmbedAuthor) and len(self.author.name) > 256:
            errors['author.name'] = f'Author name length is {len(self.author.name)}, maximum is 256.'

        counter = 0
        counter += len(self.title) if self.title is not None else 0
        counter += len(self.description) if self.description is not None else 0

        if self.fields is not None:
            for x in range(len(self.fields)):
                counter += len(self.fields[x].name) + len(self.fields[x].value)

        counter += len(self.footer.text) if isinstance(self.footer, MessageEmbedFooter) else 0
        counter += len(self.author.name) if isinstance(self.author, MessageEmbedAuthor) else 0
        if counter > 6000:
            errors['total'] = f'Total length is {counter}, maximum is 6000.'

        if errors:
            raise MessageEmbedLimitError('Embed limits exceeded.', errors)
        
#-----------------------------------------------------------------------------------------------------------------
class MessageEmbedFooter(BaseResourceObject):
    __slots__ = ('text', 'icon_url', 'proxy_icon_url')

    def __init__(self, **kwargs):
        self.text: str                      = kwargs.get('text', None)
        self.icon_url: Optional[str]        = kwargs.get('icon_url', None)
        self.proxy_icon_url: Optional[str]  = kwargs.get('proxy_icon_url', None)

#-----------------------------------------------------------------------------------------------------------------
class MessageEmbedImage(BaseResourceObject):
    __slots__ = ('url', 'proxy_url', 'height', 'width')

    def __init__(self, **kwargs):
        self.url: str                   = kwargs.get('url')
        self.proxy_url: Optional[str]   = kwargs.get('proxy_url', None)
        self.height: Optional[int]      = kwargs.get('height', None)
        self.width: Optional[int]       = kwargs.get('width', None)

#-----------------------------------------------------------------------------------------------------------------
class MessageEmbedThumbnail(BaseResourceObject):
    __slots__ = ('url', 'proxy_url', 'height', 'width')
    def __init__(self, **kwargs):
        self.url: str                   = kwargs.get('url')
        self.proxy_url: Optional[str]   = kwargs.get('proxy_url', None)
        self.height: Optional[int]      = kwargs.get('height', None)
        self.width: Optional[int]       = kwargs.get('width', None)

#-----------------------------------------------------------------------------------------------------------------\
class MessageEmbedVideo(BaseResourceObject):
    __slots__ = ('url', 'proxy_url', 'height', 'width')
    def __init__(self, **kwargs):
        self.url: str                   = kwargs.get('url')
        self.proxy_url: Optional[str]   = kwargs.get('proxy_url', None)
        self.height: Optional[int]      = kwargs.get('height', None)
        self.width: Optional[int]       = kwargs.get('width', None)

#-----------------------------------------------------------------------------------------------------------------
class MessageEmbedProvider(BaseResourceObject):
    __slots__ = ('name', 'url')
    def __init__(self, **kwargs):
        self.name: Optional[str] = kwargs.get('name', None)
        self.url: Optional[str] = kwargs.get('url', None)

#-----------------------------------------------------------------------------------------------------------------
class MessageEmbedAuthor(BaseResourceObject):
    __slots__ = ('name', 'url', 'icon_url', 'proxy_icon_url')
    def __init__(self, **kwargs):
        self.name: str =                        kwargs.get('name')
        self.url: Optional[str] =               kwargs.get('url', None)
        self.icon_url: Optional[str] =          kwargs.get('icon_url', None)
        self.proxy_icon_url: Optional[str] =    kwargs.get('proxy_icon_url', None)

#-----------------------------------------------------------------------------------------------------------------
class MessageEmbedField(BaseResourceObject):
    __slots__ = ('name', 'value', 'inline')
    def __init__(self, **kwargs):
        self.name: str =                kwargs.get('name')
        self.value: str =               kwargs.get('value')
        self.inline: Optional[str] =    kwargs.get('inline', None)

#-----------------------------------------------------------------------------------------------------------------
class Reaction(BaseResourceObject):
    __slots__ = ('count', 'count_details', 'me', 'me_burst', 'emoji', 'burst_colors')

    def __init__(self, **kwargs):
        self.count: int =                           kwargs.get('count', 0)
        self.count_details: ReactionCountDetails =  ReactionCountDetails(**kwargs.get('count_details')) if 'count_details' in kwargs and kwargs['count_details'] is not None else ReactionCountDetails()
        self.me: bool =                             kwargs.get('me', False)
        self.me_burst: bool =                       kwargs.get('me_burst', False)
        self.emoji: PartialEmoji =                  Emoji(**kwargs.get('emoji'))
        self.burst_colors: List[str] =              kwargs.get('burst_colors', list())

#-----------------------------------------------------------------------------------------------------------------
class ReactionCountDetails(BaseResourceObject):
    __slots__ = ('burst', 'normal')
    def __init__(self, **kwargs):
        self.burst: int =    kwargs.get('burst', 0)
        self.normal: int =   kwargs.get('normal', 0)

#-----------------------------------------------------------------------------------------------------------------
class MessageActivity(BaseResourceObject):
    __slots__ = ('type', 'party_id')
    def __init__(self, **kwargs):
        self.type: int =          kwargs.get('type')
        self.party_id: Optional[str] =      kwargs.get('party_id', None)

#-----------------------------------------------------------------------------------------------------------------
class MessageReference(BaseResourceObject):
    __slots__ = ('type', 'message_id', 'channel_id', 'guild_id', 'fail_if_not_exists')
    def __init__(self, **kwargs):
        self.type: Optional[int] =                  kwargs.get('type', None)
        self.message_id: Snowflake =                kwargs.get('message_id', None)
        self.channel_id: Snowflake =                kwargs.get('channel_id', None)
        self.guild_id: Optional[Snowflake] =        kwargs.get('guild_id', None)
        self.fail_if_not_exists: Optional[bool] =   kwargs.get('fail_if_not_exists', None)

#-----------------------------------------------------------------------------------------------------------------
class MessageSnapshot(BaseResourceObject):
    __slots__ = ('message')

    def __init__(self, **kwargs):
        self.message: List[PartialMessage] = [PartialMessage(**x) for x in kwargs.get('message')]

#-----------------------------------------------------------------------------------------------------------------
class MessageStickerItem(BaseResourceObject):
    __slots__ = ('id', 'name', 'format_type')

    def __init__(self, **kwargs):
        self.id: Snowflake =    kwargs.get('id')
        self.name: str =        kwargs.get('name')
        self.format_type: int = kwargs.get('format_type')

#-----------------------------------------------------------------------------------------------------------------
class MessageRoleSubscription(BaseResourceObject):
    __slots__ = ('role_subscription_listing_id', 'tier_name', 'total_months_subscribed', 'is_renewal')

    def __init__(self, **kwargs):
        self.role_subscription_listing_id: Snowflake =  kwargs.get('role_subscription_listing_id')
        self.tier_name: str =                           kwargs.get('tier_name')
        self.total_months_subscribed: int =             kwargs.get('total_months_subscribed')
        self.is_renewal: bool =                         kwargs.get('is_renewal')

#-----------------------------------------------------------------------------------------------------------------
class MessageResolved(BaseResourceObject):
    #NOTE: This requires a bunch of partials rather than what is passed via kwargs. 
    #      This is a placeholder for now.
    #      Check https://discord.com/developers/docs/interactions/receiving-and-responding#interaction-object-resolved-data-structure for the structure
    def __init__(self, **kwargs):
        self.users = kwargs.get('users')
        self.members = kwargs.get('members')
        self.roles = kwargs.get('roles')
        self.channels = kwargs.get('channels')
        self.messages = kwargs.get('messages')
        self.attachments = kwargs.get('attachments')

#-----------------------------------------------------------------------------------------------------------------
class MessageReactionRemove(BaseResourceObject):
    __slots__ = (
        'user_id',
        'channel_id',
        'message_id',
        'guild_id',
        'emoji',
        'burst',
        'type'
    )

    def __init__(self, **kwargs):
        self.user_id: Snowflake             = kwargs.get('user_id')
        self.channel_id: Snowflake          = kwargs.get('channel_id')
        self.message_id: Snowflake          = kwargs.get('message_id')
        self.guild_id: Optional[Snowflake]  = kwargs.get('guild_id')
        self.emoji: PartialEmoji            = Emoji(**kwargs.get('emoji'))
        self.burst: bool                    = kwargs.get('burst', False)
        self.type: int                      = kwargs.get('type', 0)

#-----------------------------------------------------------------------------------------------------------------
class MessageReactionAdd(BaseResourceObject):
    __slots__ = (
        'user_id',
        'channel_id',
        'message_id',
        'guild_id',
        'member',
        'emoji',
        'message_author_id',
        'burst',
        'burst_colors',
        'type'
    )

    def __init__(self, **kwargs):
        self.user_id: Snowflake                         = kwargs.get('user_id')
        self.channel_id: Snowflake                      = kwargs.get('channel_id')
        self.message_id: Snowflake                      = kwargs.get('message_id')
        self.guild_id: Optional[Snowflake]              = kwargs.get('guild_id', None)
        self.member: Optional[GuildMember]              = GuildMember(**kwargs.get('member')) if 'member' in kwargs and kwargs['member'] is not None else None
        self.emoji: PartialEmoji                        = Emoji(**kwargs.get('emoji'))
        self.message_author_id: Optional[Snowflake]     = kwargs.get('message_author_id', None)
        self.burst: bool                                = kwargs.get('burst', False)
        self.burst_colors: Optional[List[str]]          = kwargs.get('burst_colors', list()) if 'burst_colors' in kwargs and kwargs['burst_colors'] is not None else None
        self.type: int                                  = kwargs.get('type', 0)

#-----------------------------------------------------------------------------------------------------------------
class MessageReactionRemoveAll(BaseResourceObject):
    __slots__ = (
        'channel_id',
        'message_id',
        'guild_id'
    )

    def __init__(self, **kwargs):
        self.channel_id: Snowflake          = kwargs.get('channel_id')
        self.message_id: Snowflake          = kwargs.get('message_id')
        self.guild_id: Optional[Snowflake]  = kwargs.get('guild_id', None)

#-----------------------------------------------------------------------------------------------------------------
class MessageReactionRemoveEmoji(BaseResourceObject):
    __slots__ = (
        'channel_id',
        'message_id',
        'guild_id',
        'emoji'
    )

    def __init__(self, **kwargs):
        self.channel_id: Snowflake          = kwargs.get('channel_id')
        self.message_id: Snowflake          = kwargs.get('message_id')
        self.guild_id: Optional[Snowflake]  = kwargs.get('guild_id', None)
        self.emoji: PartialEmoji            = Emoji(**kwargs.get('emoji'))