from typing import List, Literal, Optional, TypedDict, Union, Dict
from typing_extensions import NotRequired, Required, Self

import yaml
from yaml import Loader
from models.base import Base

__all__ = ['ResponseCodes', 'HttpResponseCode', 'GatewayOpCode', 'GatewayCloseCode', 'VoiceOpCode', 'VoiceCloseCode', 'JsonCodes']

#-------------------------------------------------------------------------------------------
class GatewayOpCode():
    __slots__ = ('code', 'name', 'action', 'description')
    def __init__(self, code=0, name='', action=0, description=''):
        self.code: int = code
        self.name: str = name
        self.action: str = action
        self.description: str = description

#-------------------------------------------------------------------------------------------
class GatewayCloseCode():
    __slots__ = ('code', 'description', 'explanation', 'reconnect')
    def __init__(self, code=0, description='', explanation='', reconnect=False):
        self.code: int = code
        self.description: str = description
        self.explanation: str = explanation
        self.reconnect: bool = reconnect

#-------------------------------------------------------------------------------------------
class VoiceOpCode():
    __slots__ = ('code', 'name', 'sentBy', 'description', 'binary')
    def __init__(self, code=0, name='', sentBy='', description='', binary=False):
        self.code: int = code
        self.name: str = name
        self.sentBy: str = sentBy
        self.description: str = description
        self.binary: bool = binary

#-------------------------------------------------------------------------------------------
class VoiceCloseCode():
    __slots__ = ('code', 'description', 'explanation')
    def __init__(self, code=0, description='', explanation=''):
        self.code: int = code
        self.description: str = description
        self.explanation: str = explanation

#-------------------------------------------------------------------------------------------
class HttpResponseCode():
    __slots__ = ('code', 'name', 'meaning')
    def __init__(self, code=0, name='', meaning=''):
        self.code: int = code
        self.name: str = name
        self.meaning: str = meaning

#-------------------------------------------------------------------------------------------
class JsonCodes():
    __slots__ = ('code', 'meaning')
    def __init__(self, code=0, meaning=''):
        self.code: int = code
        self.meaning: str = meaning

#-------------------------------------------------------------------------------------------
class ResponseCodes(Base):
    __slots__ = ('http_codes', 'gateway_op_codes', 'gateway_close_codes', 'voice_op_codes', 'voice_close_codes', 'json_codes')
    
    def __init__(self):
        self.http_codes: Dict[int, HttpResponseCode] = self._init_http_codes()
        self.gateway_op_codes: Dict[int, GatewayOpCode] = self._init_gateway_codes()
        self.gateway_close_codes: Dict[int, GatewayCloseCode] = self._init_gateway_close_codes()
        self.voice_op_codes: Dict[int, VoiceOpCode] = self._init_voice_codes()
        self.voice_close_codes: Dict[int, VoiceCloseCode] = self._init_voice_close_codes()
        self.json_codes: Dict[int, JsonCodes] = self._init_json_codes()
    
    #-----------------------------------------------------------------
    #   HTTP Codes
    #-----------------------------------------------------------------
    def _init_http_codes(self) -> Dict[int, HttpResponseCode]:
        httpCodeObjects = dict()
        with open('./config/httpCodes.yaml', 'r') as f:
            for x in yaml.load_all(f, Loader=Loader):
                for code in x:
                    httpCodeObjects[code['code']] = HttpResponseCode(**code)
        return httpCodeObjects

    #-----------------------------------------------------------------
    #   Gateway Op Codes
    #-----------------------------------------------------------------
    def _init_gateway_codes(self) -> Dict[int, GatewayOpCode]:
        gatewayCodes = dict()
        with open('./config/gateOpCodes.yaml', 'r') as f:
            for x in yaml.load_all(f, Loader=Loader):
                for code in x:
                    gatewayCodes[code['code']] = GatewayOpCode(**code)
        return gatewayCodes

    #-----------------------------------------------------------------
    #   Gateway Close Codes
    #-----------------------------------------------------------------
    def _init_gateway_close_codes(self) -> Dict[int, GatewayCloseCode]:
        gatewayCloseCodes = dict()
        with open('./config/gateCloseCodes.yaml', 'r') as f:
            for x in yaml.load_all(f, Loader=Loader):
                for code in x:
                    gatewayCloseCodes[code['code']] = GatewayCloseCode(**code)
        return gatewayCloseCodes
    
    #-----------------------------------------------------------------
    #   Voice Op Codes
    #-----------------------------------------------------------------
    def _init_voice_codes(self) -> Dict[int, VoiceOpCode]:
        voiceCodes = dict()
        with open('./config/voiceOpCodes.yaml', 'r') as f:
            for x in yaml.load_all(f, Loader=Loader):
                for code in x:
                    voiceCodes[code['code']] = VoiceOpCode(**code)
        return voiceCodes
    
    #-----------------------------------------------------------------
    #   Voice Close Codes
    #-----------------------------------------------------------------
    def _init_voice_close_codes(self) -> Dict[int, VoiceCloseCode]:
        voiceCloseCodes = dict()
        with open('./config/voiceCloseCodes.yaml', 'r') as f:
            for x in yaml.load_all(f, Loader=Loader):
                for code in x:
                    voiceCloseCodes[code['code']] = VoiceCloseCode(**code)
        return voiceCloseCodes

    #-----------------------------------------------------------------
    #   JSON Codes
    #-----------------------------------------------------------------
    def _init_json_codes(self) -> Dict[int, JsonCodes]:
        jsonCodes = dict()
        with open('./config/jsonCodes.yaml', 'r') as f:
            for x in yaml.load_all(f, Loader=Loader):
                for code in x:
                    jsonCodes[code['code']] = JsonCodes(**code)
        return jsonCodes

    def get_op_obj(self, type, code) -> Union[GatewayOpCode, VoiceOpCode]:
        codes = self._to_dict()
        return codes[type][code]