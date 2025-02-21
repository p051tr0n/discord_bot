import config
from typing import Any
from models.base import Base
from models.bot.events.gateway_event import GatewayEvent
from models.bot.events.presence import Presence
from models.bot.activities.activity import Activity

class ConnectionProperties(Base):

    def __init__(self, **kwargs: Any) -> ConnectionProperties:
        super().__init__(**kwargs)    
        self.os = kwargs.pop('os', 'linux')
        self.browser = kwargs.pop('browser', 'squirrel_bot')
        self.device = kwargs.pop('device', 'squirrel_bot')
#--------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------
class IdentifyEvent(GatewayEvent):
    '''
        Represents the Identify Payload Structure defined here: https://discord.com/developers/docs/topics/gateway#identify-identify-structure
    '''
    def __init__(self, **kwargs: Any) -> IdentifyEvent:
        '''
            token: str
                The authentication token.
            
            intents: int
                The Gateway Intents.
                https://discord.com/developers/docs/events/gateway#gateway-intents
            
            properties: ConnectionProperties
                The connection properties.
            
            compress: bool
                Whether this connection supports compression of packets.
            
            large_threshold: int
                The threshold at which the Gateway will stop sending offline members in the guild member list.
            
            shard: list
                The shard information.
                https://discord.com/developers/docs/events/gateway#sharding
            
            presence: Presence
                The presence structure for initial presence information.
            
            guild_subscriptions: bool
                Whether the client should receive member information.
            
            heartbeat_interval: int
                The interval (in milliseconds) the client should heartbeat with.
        '''
        if not self.checekValidIdentifyEvent(**kwargs):
            #TODO: Log this error object
            objs = {k: v for k, v in kwargs.items()}
            errLogMsg = self._create_error_message('Invalid Identify Event.', objs)
            raise ValueError('Invalid Identify Event.')

        super().__init__(config.RESPONSE_CODES.gateway_op_codes['Identify'], None, None, **kwargs)
        
        self.token = kwargs.pop('token', config.OPTS['botToken'])
        self.intents = kwargs.pop('intents', 0)
        self.properties = ConnectionProperties.(**kwargs.pop('properties', dict()))
        self.compress = kwargs.pop('compress', False)
        self.large_threshold = kwargs.pop('large_threshold', 50)
        self.shard = kwargs.pop('shard', None)
        self.presence = Presence.(**kwargs.pop('presence', dict()))
        self.heartbeat_interval = kwargs.pop('heartbeat_interval', None)

    #-------------------------------------------------------------------------------
    def checekValidIdentifyEvent(self, **kwargs) -> bool:
        '''
            Check if the Identify Event is valid.
        '''
        token = kwargs.get('token', None)
        properties = kwargs.get('properties', None)
        intents = kwargs.get('intents', None)

        if (not token or not properties or not intents):
            return False
        return True

#--------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------
class ResumeEvent(GatewayEvent):
    '''
        Represents the Resume Payload Structure defined here: https://discord.com/developers/docs/topics/gateway#resume-resume-structure
    '''
    def __init__(self, **kwargs: Any) -> ResumeEvent:
        '''
            token: str
                The authentication token.

            session_id: str
                The session id.

            seq: int
                The last sequence number received.
        '''
        if not self.checekValidResumeEvent(token, session_id, seq):
            #TODO: Log this error object
            objs = {k: v for k, v in kwargs.items()}
            errLogMsg = self._create_error_message('Invalid Resume Event.', objs)
            raise ValueError('Invalid Resume Event.')

        super().__init__(config.RESPONSE_CODES.gateway_op_codes['Resume'], None, None, **kwargs)

        self.token = kwargs.pop('token', config.OPTS['botToken'])
        self.session_id = kwargs.pop('session_id', None)
        self.seq = kwargs.pop('seq', None)

    #-------------------------------------------------------------------------------
    def checekValidResumeEvent(self, **kwargs) -> bool:
        '''
            Check if the Resume Event is valid.
        '''
        token = kwargs.get('token', None)
        session_id = kwargs.get('session_id', None)
        seq = kwargs.get('seq', None)
        if (not token or not session_id or not seq):
            return False
        return True

#--------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------
class HeartbeatEvent(GatewayEvent):
    '''
        Represents the Heartbeat Payload Structure defined here: https://discord.com/developers/docs/topics/gateway#heartbeat-heartbeat-structure
    '''
    def __init__(self,**kwargs) -> HeartbeatEvent:
        '''
            seq: int
                The last sequence number received.
        '''
        
        super().__init__(config.RESPONSE_CODES.gateway_op_codes['Heartbeat'], None, None, **kwargs)

        self.seq = kwargs.pop('seq', None)

#--------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------
class RequestGuildMemberEvent(GatewayEvent):
    '''
        Represents the Request Guild Members Payload Structure defined here: https://discord.com/developers/docs/topics/gateway#request-guild-members-guild-request-members-structure
    '''
    def __init__(self, **kwargs) -> RequestGuildMemberEvent:
        '''
            guild_id: str
                The id of the guild.

            query: str
                String that username starts with, or an empty string to return all members.

            limit: int
                Maximum number of members to send matching the query; a limit of 0 can be used with an empty string query to return all members.

            presences: bool
                Whether to include the presences of the matched members.

            user_ids: list
                Array of user ids to fetch.

            nonce: str
                String to identify the request.
        '''
        if not self.checekValidRequestGuildMemberEvent(**kwargs):
            #TODO: Log this error object
            objs = {k: v for k, v in kwargs.items()}
            errLogMsg = self._create_error_message('Invalid RequestGuildMember Event.', objs)
            raise ValueError('Invalid RequestGuildMember Event.')

        super().__init__(config.RESPONSE_CODES.gateway_op_codes['Request Guild Members'], None, None, **kwargs)

        self.guild_id = kwargs.pop('guild_id', None)
        self.query = kwargs.pop('query', '')
        self.limit = kwargs.pop('limit', 0)
        self.presences = kwargs.pop('presences', False)
        self.user_ids = kwargs.pop('user_ids', None)
        self.nonce = kwargs.pop('nonce', None)


    #-------------------------------------------------------------------------------
    def checekValidRequestGuildMemberEvent(self,**kwargs) -> bool:
        '''
            Check if the Request Guild Member Event is valid.
        '''
        guild_id = kwargs.get('guild_id', None)
        nonce = kwargs.get('nonce', None)

        if (not guild_id):
            return False
        if nonce:
            if len(nonce.encode('utf-8')) > 32:
                return False
        return True

#--------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------
class UpdateVoiceStateEvent(GatewayEvent):
    '''
        Represents the Update Voice State Payload Structure defined here: https://discord.com/developers/docs/topics/gateway#update-voice-state-voice-state-update-structure
    '''
    def __init__(self, **kwargs) -> UpdateVoiceStateEvent:
        '''
            guild_id: str
                The id of the guild.

            channel_id: str
                The id of the voice channel.

            self_mute: bool
                Whether the client is muted.

            self_deaf: bool
                Whether the client is deafened.
        '''
        if not self.checekValidUpdateVoiceStateEvent(guild_id, channel_id):
            #TODO: Log this error object
            objs = {k: v for k, v in kwargs.items()}
            errLogMsg = self._create_error_message('Invalid UpdateVoiceState Event.', objs)
            raise ValueError('Invalid UpdateVoiceState Event.')
    
        super().__init__(config.RESPONSE_CODES.gateway_op_codes['Voice Status Update'], None, None, **kwargs)

        self.guild_id = kwargs.pop('guild_id', None)
        self.channel_id = kwargs.pop('channel_id', None)
        self.self_mute = kwargs.pop('self_mute', False)
        self.self_deaf = kwargs.pop('self_deaf', False)

    #-------------------------------------------------------------------------------
    def checekValidUpdateVoiceStateEvent(self,**kwargs) -> bool:
        '''
            Check if the Update Voice State Event is valid.
        '''
        guild_id = kwargs.get('guild_id', None)
        channel_id = kwargs.get('channel_id', None)
        if (not guild_id or not channel_id):
            return False
        return True

#--------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------
class UpdateStatusEvent(GatewayEvent):
    '''
        Represents the Update Status Payload Structure defined here: https://discord.com/developers/docs/topics/gateway#update-status-status-update-structure
    '''
    def __init__(self, **kwargs) -> UpdateStatusEvent:
        '''
            since: int
                Unix time (in milliseconds) of when the client went idle, or null if the client is not idle.

            activities: list
                The user's activities.

            status: str
                The user's new status.

            afk: bool
                Whether or not the client is afk.
        '''
        try:
            newPresence = Presence(**kwargs)
        except ValueError as e:
            errLogMsg = self._create_error_message('Invalid UpdateStatus Event.', e)
            raise ValueError(e)

        super().__init__(config.RESPONSE_CODES.gateway_op_codes['Presence Update'], None, None, **newPresence._to_dict())

        self.since = kwargs.pop('since', None)
        self.activities = [Activity(**x) for x in kwargs.pop('activities', list())]
        self.status = kwargs.pop('status', None)
        self.afk = kwargs.pop('afk', False)