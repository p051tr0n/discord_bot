from typing import List, Union, Dict, Generator, Any
from typing_extensions import NotRequired, Self

from src.models.base import Base
from src.endpoints.message import ChannelMessage
from tornado.httpclient import HTTPRequest
from src.obj_types.proc_event import HttpEvent


__all__ = ['ListenerFilter', 'ListenerAction', 'ListenerObject']

#-----------------------------------------------------------------------------------------------------------
class ListenerFilter(Base):
    '''
        ListenerFilter object that will be used to filter events that are detected.

        condition -> The condition to apply to the filters. Used to loop through the fields and determine if the event passes.
        fields -> The fields to apply the filters to

        Supported conditions:
            equals -> The field must equal the value
            contains -> The field must contain the value
            contains_any -> The field must contain any of the values
    '''
    __slots__ = ('condition', 'fields')

    def __init__(self, **kwargs):
        self.condition = kwargs.get('condition')
        self.fields = kwargs.get('fields')

#-----------------------------------------------------------------------------------------------------------
class ListenerAction(Base):
    '''
        ListenerAction object that will be used to define the actions to take when an event is detected.

        type -> The type of action to take
        data -> The data to use for the action. Should be a dictionary object that corresponds to an HTTP API Event object.
    '''
    __slots__ = ('type', 'data', 'chanMessage', 'mapping')

    def __init__(self, chanMessage, **kwargs):
        self.type = kwargs.get('type')
        self.data = kwargs.get('data')
        self.chanMessage = chanMessage

        self.mapping = {
            "SEND_MESSAGE": self.chanMessage.createChannelMessage,
            "ADD_REACTION": self.chanMessage.createReaction
        }
    
    #-------------------------------------------------------------------------------------------
    def createRequest(self, event: HttpEvent) -> HTTPRequest:
        '''
            Create and return an HTTPRequest object based on the action type and data.
        '''
        return self.mapping[self.type](event, **self.data)

#-----------------------------------------------------------------------------------------------------------
class ListenerObject(Base):
    '''
        Listener object that will be used to listen for specific events.

        type -> The type of event to listen for
        filter -> The filters to apply to the event
        action -> The actions to take when the event is detected and passes the filters
    '''
    __slots__ = ('type', 'filters', 'actions', 'chanMessage')

    def __init__(self, chanMessage, **kwargs):
        self.chanMessage = chanMessage
        self.type = kwargs.get('type')
        self.filters = [ListenerFilter(**x) for x in kwargs.get('filter')]
        self.actions = [ListenerAction(self.chanMessage, **x) for x in kwargs.get('actions')]

    #-------------------------------------------------------------------------------------------
    def check(self, event: HttpEvent) -> bool:
        '''
            Check the event against the listener's filters.
            Use the generator created with self.checkFilters(event) and loop over it.
            If any of the values are False, return False.

            event -> HTTP
        '''
        for result in self.checkFilters(event.data._to_dict()):
            if not result:
                return False
        return True

    #-------------------------------------------------------------------------------------------
    def checkFilters(self, event: Dict) -> Generator[bool, None, bool]:
        '''
        '''
        #----------------------------------------------------
        # Check each filter
        #----------------------------------------------------
        for filterObj in self.filters:

            for field_key, field_val in filterObj.fields.items():

                result = self.traverseFields(event, field_key, field_val)

                if not result:
                    yield False

                if filterObj.condition.lower() == "equals":
                    yield result[0] == result[1]

                elif filterObj.condition.lower() == "contains":
                    yield result[1] in result[0]

                elif filterObj.condition.lower() == "contains_any":
                    for val in result[1]:
                        yield val in result[0]


    def traverseFields(self, obj: Any, key=None, val=None):
        '''
            obj -> the event or section of the event being searched.
            key -> the key from the filter field object that is being searched for in the event.
            val -> the value from the filter field object that is being searched for in the event.
        '''
        # if the key is missing from the event obj, then anything inside the value
        # will not be found either so return false.
        if key not in obj:
            return False

        elif isinstance(val, dict):            
            # the key does exist in the event, so loop to the next level.
            for k, v in val.items():
                return self.traverseFields(obj[key], k, v)
        else:
            return [obj[key], val]