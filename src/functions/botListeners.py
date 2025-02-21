import yaml
from yaml import Loader

from typing import List, Generator
from models.bot.listener import ListenerObject
from endpoints.message import ChannelMessage
from obj_types.proc_event import HttpEvent

class BotListeners(object):
    '''
        Serializes listeners for the bot from the listeners.yaml file.

        Entry Formats:
            - type: <event type>
              filter:
                - condition: <equals, contains, contains_any>
                  fields: 
                    <field key>: <field value>
                    <field key>: 
                        <subfield key>: <subfield value>
                ...
              actions:
                - type: <ACTION_TYPE>
                  data:
                    <field>: <value>
                ...

        filters fields should match the fields in an event object that you wish to match against based on the condition specified.
        actions define how to react to the event should the filter match up.
        the data section of an action should be capable of being serialized into an HTTP API Event object.
    '''

    __slots__ = ('listeners', 'chanMessage')

    def __init__(self):
        self.listeners = list()
        self.chanMessage = ChannelMessage()
        self.loadListeners()

    #-------------------------------------------------------------------------------------------
    def loadListeners(self):
        '''
            Load the listeners from the listeners.yaml file.
        '''
        with open('config/listeners.yaml', 'r+') as file:
            yamlListeners = yaml.load(file, Loader=Loader)
            if yamlListeners is None:
                return
            for x in yamlListeners:
                self.listeners.append(ListenerObject(self.chanMessage, **x))

    #-------------------------------------------------------------------------------------------
    def checkListeners(self, event: HttpEvent) -> Generator[ListenerObject, None, None]:
        '''
            Check the event against the listeners.
        '''
        # x is a ListenerObject
        for x in self.listeners:
            if x.check(event):
                # can send the event to the listener action here and have it create the request object
                for action in x.actions:
                    yield action.createRequest(event.data)