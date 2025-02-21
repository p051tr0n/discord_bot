import json
import config

from models.bot.events.gateway_event import GatewayEvent


from models.bot.resources.auto_moderation import AutoModerationActionExecution, AutoModerationRule
from models.bot.resources.entitlement import Entitlement
from models.bot.resources.guild import (
    Guild,
    GuildCreate, 
    GuildAuditLogEntry, 
    GuildBan, 
    GuildEmojis, 
    GuildStickers,
    GuildRole,
    GuildRoleDelete,
    GuildScheduledEvent,
    GuildScheduledEventUser,
    GuildSoundboardSoundDelete,
    GuildSoundboardSounds)
from models.bot.resources.channel import Channel, ThreadListSync, ThreadMember, ThreadMembersUpdate, ChannelPinsUpdate
from models.bot.resources.soundboard import SoundboardSound
from models.bot.resources.user import User, GuildMemberRemove, GuildMemberAdd
from models.bot.resources.presence import Presence, Typing
from models.bot.resources.message import *



__all__ = ['EventGenerator']

class EventGenerator(object):

    event_map = {
            "AUTO_MODERATION_RULE_CREATE": AutoModerationRule,
            "AUTO_MODERATION_RULE_UPDATE": AutoModerationRule,
            "AUTO_MODERATION_RULE_DELETE": AutoModerationRule,
            "AUTO_MODERATION_ACTION_EXECUTE": AutoModerationActionExecution,
            "CHANNEL_CREATE": Channel,
            "CHANNEL_UPDATE": Channel,
            "CHANNEL_DELETE": Channel,
            "THREAD_CREATE": Channel,
            "THREAD_UPDATE": Channel,
            "THREAD_DELETE": Channel,
            "THREAD_LIST_SYNC": ThreadListSync,
            "THREAD_MEMBER_UPDATE": ThreadMember,
            "THREAD_MEMBERS_UPDATE": ThreadMembersUpdate,
            "CHANNEL_PINS_UPDATE": ChannelPinsUpdate,
            "ENTITLEMENT_CREATE": Entitlement,
            "ENTITLEMENT_UPDATE": Entitlement,
            "ENTITLEMENT_DELETE": Entitlement,
            "GUILD_CREATE": GuildCreate,
            "GUILD_UPDATE": Guild,
            "GUILD_DELETE": Guild,
            "GUILD_AUDIT_LOG_ENTRY_CREATE": GuildAuditLogEntry,
            "GUILD_BAN_ADD": GuildBan,
            "GUILD_BAN_REMOVE": GuildBan,
            "GUILD_EMOJIS_UPDATE": GuildEmojis,
            "GUILD_STICKERS_UPDATE": GuildStickers,
            "GUILD_INTEGRATIONS_UPDATE": None,
            "GUILD_MEMBER_ADD": GuildMemberAdd,
            "GUILD_MEMBER_REMOVE": GuildMemberRemove,
            "GUILD_MEMBER_UPDATE": GuildMemberAdd,
            "GUILD_MEMBERS_CHUNK": None,
            "GUILD_ROLE_CREATE": GuildRole,
            "GUILD_ROLE_UPDATE": GuildRole,
            "GUILD_ROLE_DELETE": GuildRoleDelete,
            "GUILD_SCHEDULED_EVENT_CREATE": GuildScheduledEvent,
            "GUILD_SCHEDULED_EVENT_UPDATE": GuildScheduledEvent,
            "GUILD_SCHEDULED_EVENT_DELETE": GuildScheduledEvent,
            "GUILD_SCHEDULED_EVENT_USER_ADD": GuildScheduledEventUser,
            "GUILD_SCHEDULED_EVENT_USER_REMOVE": GuildScheduledEventUser,
            "GUILD_SOUNDBOARD_SOUND_CREATE": SoundboardSound,
            "GUILD_SOUNDBOARD_SOUND_UPDATE": SoundboardSound,
            "GUILD_SOUNDBOARD_SOUND_DELETE": GuildSoundboardSoundDelete,
            "GUILD_SOUNDBOARD_SOUNDS_UPDATE": GuildSoundboardSounds,
            "SOUNDBOARD_SOUNDS": GuildSoundboardSounds,
            "INTEGRATION_CREATE": None,
            "INTEGRATION_UPDATE": None, 
            "INTEGRATION_DELETE": None,
            "INTERACTION_CREATE": None,
            "INVITE_CREATE": None,
            "INVITE_DELETE": None,
            "MESSAGE_CREATE": Message,
            "MESSAGE_UPDATE": Message,
            "MESSAGE_DELETE": Message,
            "MESSAGE_DELETE_BULK": Message,
            "MESSAGE_REACTION_ADD": MessageReactionAdd,
            "MESSAGE_REACTION_REMOVE": MessageReactionRemove,
            "MESSAGE_REACTION_REMOVE_ALL": MessageReactionRemoveAll,
            "MESSAGE_REACTION_REMOVE_EMOJI": MessageReactionRemoveEmoji,
            "PRESENCE_UPDATE": Presence,
            "STAGE_INSTANCE_CREATE": None,
            "STAGE_INSTANCE_UPDATE": None,
            "STAGE_INSTANCE_DELETE": None,
            "SUBSCRIPTION_CREATE": None,
            "SUBSCRIPTION_UPDATE": None,
            "SUBSCRIPTION_DELETE": None,
            "TYPING_START": Typing,
            "USER_UPDATE": User,
            "VOICE_CHANNEL_EFFECT_SEND": None,
            "VOICE_STATE_UPDATE": None,
            "VOICE_SERVER_UPDATE": None,
            "WEBHOOKS_UPDATE": None,
            "MESSAGE_POLL_VOTE_ADD": None,
            "MESSAGE_POLL_VOTE_REMOVE": None
        }

    #-------------------------------------------------------------------------------------------
    @classmethod
    def createResource(cls, event: dict):
        '''
            Create a resource object based on the vent.
        '''
        return cls.event_map.get(event.t)(**event.d) if event.t in cls.event_map else None


    #-------------------------------------------------------------------------------------------
    @classmethod
    def incoming_event(cls, event: dict) -> GatewayEvent:
        '''
            Create a GatewayEvent object from the incoming event.
        '''
        if isinstance(event, dict):
            return GatewayEvent(**event)
        elif isinstance(event, GatewayEvent):
            return event
        elif isinstance(event, str):
            return GatewayEvent(**json.loads(event))

    #-------------------------------------------------------------------------------------------
    @classmethod
    def auth_event(cls) -> GatewayEvent:
        '''
            Create an auth event.
        '''
        event_data = {
                        "token": config.OPTS['botToken'],
                        "properties": {
                            "$os": "linux",
                            "$browser": "disco",
                            "$device": "disco"
                        },
                        "presence": {
                            "status": "online",
                            "afk": False
                        }
                    }

        return GatewayEvent(2, None, None, event_data)

    #-------------------------------------------------------------------------------------------
    @classmethod
    def heartbeat_event(cls, sequence) -> GatewayEvent:
        '''
            Create an event for sending a heartbeat.
        '''
        return GatewayEvent(1, None, sequence, None)
    
    #-------------------------------------------------------------------------------------------
    @classmethod
    def resume_event(cls, sequence, session_id) -> GatewayEvent:
        '''
            Create an event for resuming a session.
        '''
        event_data = {
                        "token": config.OPTS['botToken'],
                        "session_id": session_id,
                        "seq": sequence
                    }
        return GatewayEvent(6, None, None, event_data)
