import config
from models.base import Base
from models.bot.user import User
from models.bot.guild import PartialGuild
from models.bot.application import PartialApplication
from models.bot.events.gateway_event import GatewayEvent

class Hello(GatewayEvent):
    def __init__(self, **kwargs):
        '''
            Represents the Hello Structure defined here: https://discord.com/developers/docs/topics/gateway#hello

            heartbeat_interval: int
                The interval (in milliseconds) the client should heartbeat with.
        '''
        super().__init__(config.RESPONSE_CODES.gateway_op_codes['Hello'], None, None, **kwargs)
        self.heartbeat_interval = kwargs.pop('heartbeat_interval', 0)

#--------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------
class Ready(GatewayEvent):
    def __init__(self, **kwargs):
        '''
            Represents the Ready Structure defined here: https://discord.com/developers/docs/topics/gateway#ready

            v: int
                Gateway version
            user: User
                Information about the user including email, username, discriminator, etc.
            guilds: List[Guild]
                List of guilds the user is in
            session_id: str
                The session id for the user's session
            shard: List[int]
                The shard information associated with this session, if sent
        '''
        super().__init__(0, None, None, **kwargs)
        self.v = kwargs.pop('v', 0)
        self.user = User(**kwargs.pop('user', dict()))
        self.guilds = [PartialGuild(**x) for x in kwargs.pop('guilds', list())]
        self.session_id = kwargs.pop('session_id', '')
        self.shard = kwargs.pop('shard', list())
        self.application = PartialApplication(**kwargs.pop('application', dict()))

#--------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------
class Resumed(GatewayEvent):
    def __init__(self, **kwargs):
        '''
            Represents the Resumed Structure defined here: https://discord.com/developers/docs/topics/gateway#resumed
        '''
        super().__init__(9, None, None, **kwargs)

#--------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------
class Reconnect(GatewayEvent):
    def __init__(self, **kwargs):
        '''
            Represents the Reconnect Structure defined here: https://discord.com/developers/docs/topics/gateway#reconnect
        '''
        super().__init__(config.RESPONSE_CODES.gateway_op_codes['Reconnect'],
                        None,
                        None,
                        **kwargs)

#--------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------
class InvalidSession(GatewayEvent):
    def __init__(self, **kwargs):
        '''
            Represents the Invalid Session Structure defined here: https://discord.com/developers/docs/topics/gateway#invalid-session
            resumable: bool
                Whether the session can be resumed
        '''
        super().__init__(config.RESPONSE_CODES.gateway_op_codes['Invalid Session'],
                        None,
                        None,
                        **kwargs)
        self.resumable = kwargs.pop('resumable', False)