import json
import config
from src.models.base import Base

class GatewayEvent(Base):
    '''
        Base class for all gateway events.

        Represents the Payload Structure defined here: https://discord.com/developers/docs/events/gateway-events#payload-structure
    '''

    def __init__(self, op = None, t = None, s = None, d = None):
        '''
            s and t are None when op is not 0.
        '''
        self.op = op
        self.t = t
        self.s = s
        self.d = d

    #-------------------------------------------------------------------------------
    def checkPayloadSize(self) -> bool:
        '''
            Check if the payload size is within the limits.
        '''
        return len(self._to_json().encode('utf-8')) <= 4096

    #-------------------------------------------------------------------------------
    def _to_payload(self) -> str:
        '''
            Convert the GatewayEvent to a payload.
        '''
        if self.checkPayloadSize():
            return json.dumps(self._to_dict())
        else:
            raise ValueError('Payload size is too large.')

    #-------------------------------------------------------------------------------
    def _to_dict(self) -> dict:
        '''
            Convert the GatewayEvent to a dict.
        '''
        eventDict = dict()

        if self.op is None:
            raise ValueError('op is required.')
        else:
            eventDict['op'] = self.op

        if self.t is not None:
            eventDict['t'] = self.t

        if self.s is not None:
            eventDict['s'] = self.s

        eventDict['d'] = self.d

        return eventDict