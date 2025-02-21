import config

from models.procs.event import LogEvent, ProcessEvent, HttpEvent

from obj_types.events import GatewayEvent
from models.base import BaseResourceObject

__all__ = ['EventHandler']

class EventHandler(object):

    __slots__ = ('logQueue', 'dbQueue', 'httpQueue')

    def __init__(self, logQueue, dbQueue, httpQueue):
        self.logQueue = logQueue
        self.dbQueue = dbQueue
        self.httpQueue = httpQueue
        

    #-------------------------------------------------------------------------------------------
    def handle_event(self, eventType: str, eventData: BaseResourceObject) -> None:
        '''
            Accept an event type and event data.
            eventType -> The type of Gateway Event that was received.
            eventData -> The resource object that represents the payload of the Gateway Event.
            Create the appropriate process event that is then sent to the proper queue.
        '''

        #---------------------------------------------------
        # Check if the event type is
        # not in the GATEWAY_EVENTS
        #---------------------------------------------------
        if eventType not in config.GATEWAY_EVENTS:
            self.logQueue.put_nowait(LogEvent(action="LOG", level="ERROR", message=f"Event type {eventType} not found in GATEWAY_EVENTS"))

        #---------------------------------------------------
        # If the handler is a string
        #---------------------------------------------------
        elif isinstance(config.GATEWAY_EVENTS[eventType]['handler'], str):
            #-----------------------------------------------
            # Check if the handler is None
            #-----------------------------------------------
            if config.GATEWAY_EVENTS[eventType]['handler'] == "None":
                self.logQueue.put_nowait(LogEvent(action="LOG", level="INFO", message=f"Event type {eventType} has no handler"))
            
            #-----------------------------------------------
            # Check if the handler is HTTP
            #-----------------------------------------------
            elif config.GATEWAY_EVENTS[eventType]['handler'] == "HTTP":
                httpEvent = HttpEvent(action = "HTTP", name = eventType, data = eventData)
                self.httpQueue.put_nowait(httpEvent)

        #---------------------------------------------------
        # If the handler is a list
        #---------------------------------------------------
        elif isinstance(config.GATEWAY_EVENTS[eventType]['handler'], list):
            #-----------------------------------------------
            # Iterate through the list of handlers
            #-----------------------------------------------
            for handler in config.GATEWAY_EVENTS[eventType]['handler']:
                #-------------------------------------------
                # Check if the handler is None
                #-------------------------------------------
                if handler == "None":
                    self.logQueue.put_nowait(LogEvent(action="LOG", level="INFO", message=f"Event type {eventType} has no handler"))

                #-------------------------------------------
                # Check if the handler is HTTP
                #-------------------------------------------
                elif handler == "HTTP":
                    httpEvent = HttpEvent(action = "HTTP", name = eventType, data = eventData)
                    self.httpQueue.put_nowait(httpEvent)

                # Add in Database handler here
