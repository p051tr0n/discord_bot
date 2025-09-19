import time
import queue

import config

from multiprocessing import Process

from src.models.procs.event import LogEvent, HttpEvent, DatabaseEvent
from src.models.bot.resources.message import Message
from src.models.base import BaseResourceObject
from src.ext.listeners.botListeners import BotListeners
from src.ext.botTriggeredActions import BotTriggeredActions
from src.ext.stateHandler import StateHandler

__all__ = ['HandlerClient']

class HandlerClient(Process):
    '''
        Process for handling events from the WebSocket client.

        Ingests events from the listener queue and determines where they need to go.
    '''

    __slots__ = ('handlerQueue',
                 'logQueue',
                 'dbRequestQueue',
                 'dbResponseQueue',
                 'httpQueue',
                 'httpResponseQueue',
                 'botListeners',
                 'botCommands')

    def __init__(self, 
                 name, 
                 handlerQueue, 
                 logQueue, 
                 httpQueue, 
                 httpResponseQueue,
                 dbRequestQueue=None, 
                 dbResponseQueue=None
                ):
        super().__init__(name=name)
        self.handlerQueue = handlerQueue
        self.logQueue = logQueue
        self.dbRequestQueue = dbRequestQueue
        self.dbResponseQueue = dbResponseQueue
        self.httpQueue = httpQueue
        self.httpResponseQueue = httpResponseQueue
        self.stateHandler = StateHandler()
        self.botListeners = BotListeners()
        self.botTriggeredActions = BotTriggeredActions(httpQueue, httpResponseQueue, logQueue, self.stateHandler, dbRequestQueue=dbRequestQueue, dbResponseQueue=dbResponseQueue)
        self.botTriggeredActions.initialize_actions()


    #-------------------------------------------------------------------------------------------
    def run(self):

        while True:
            # Process events from the handler queue
            try:
                event = self.handlerQueue.get_nowait()
            except queue.Empty:
                time.sleep(0.01)  # Sleep briefly to avoid busy waiting
                continue

            if event.action == "STOP":
                break

            self.handle_event(event.eventType, event.resourceObject)


    #-------------------------------------------------------------------------------------------
    def handle_event(self, eventType: str, resourceObject: BaseResourceObject) -> None:
        '''
            Accept an event type and event data.
            eventType -> The type of Gateway Event that was received.
            resourceObject -> The resource object that represents the payload of the Gateway Event.
        '''
        #---------------------------------------------------
        # For debugging purposes
        #---------------------------------------------------
        self.logQueue.put_nowait(LogEvent(component="HANDLER", action="LOG", level="DEBUG", message=f"[EventHandler] type: {type(resourceObject)} data: {resourceObject._to_dict()}"))

        #------------------------------------------------------------------------
        #   Check if the event is an interaction
        #------------------------------------------------------------------------
        if eventType == "INTERACTION_CREATE":
            self.logQueue.put_nowait(LogEvent(component="HANDLER", action="LOG", level="DEBUG", message=f"[EventHandler] Interaction event received: {resourceObject._to_dict()}"))
            self.stateHandler.add_interaction_state(resourceObject)
            
            # Check if the user that triggered the interaction is the one that sent the command on it.

            self.botTriggeredActions.triggerableActions['interactions'][resourceObject.data.custom_id].execute(resourceObject)

        #------------------------------------------------------------------------
        #  Check if the event is for a command.
        #------------------------------------------------------------------------
        elif isinstance(resourceObject, Message) and (len(resourceObject.content) > 0 and resourceObject.content[0] == "!"):
            self.logQueue.put_nowait(LogEvent(component="HANDLER", action="LOG", level="DEBUG", message=f"[EventHandler] Command event received: {resourceObject.content}"))

            if resourceObject.content.split()[0][1:] in self.botTriggeredActions.triggerableActions['commands']:
                #----- Update the state -------
                newState = self.stateHandler.create_state(resourceObject)
                if not newState:
                    self.logQueue.put_nowait(LogEvent(component="HANDLER", action="LOG", level="ERROR", message=f"[EventHandler] State already exists for user ID: {resourceObject.author.id}"))

                self.botTriggeredActions.triggerableActions['commands'][resourceObject.content.split()[0][1:]].execute(resourceObject)

                
        #------------------------------------------------------------------------
        #  If the event is not for a command, then send for the listeners to handle.
        #------------------------------------------------------------------------
        else:
            self.logQueue.put_nowait(LogEvent(component="HANDLER", action="LOG", level="DEBUG", message=f"[EventHandler] Listener event received: {eventType}"))
            self.handle_listener_event(eventType, resourceObject)

        #---------------------------------------------------
        #       DEBUGGING
        #---------------------------------------------------
        #self.stateHandler.print_stats()

    #-------------------------------------------------------------------------------------------
    # Handle Listener Events
    #-------------------------------------------------------------------------------------------
    def handle_listener_event(self, eventType: str, resourceObject: BaseResourceObject) -> None:
        '''
            Handle a listener event.
            eventType -> The type of Gateway Event that was received.
            resourceObject -> The resource object that represents the payload of the Gateway Event.
                              This is the event that came from the Gateway API that is being processed.
        '''
        #---------------------------------------------------
        # Check if the event type is
        # not in the GATEWAY_EVENTS
        #---------------------------------------------------
        if eventType not in config.GATEWAY_EVENTS:
            self.logQueue.put_nowait(LogEvent(component="HANDLER", action="LOG", level="ERROR", message=f"[EventHandler] Event type {eventType} not found in GATEWAY_EVENTS"))
            return

        #---------------------------------------------------
        # If the handler is a string
        #---------------------------------------------------
        elif isinstance(config.GATEWAY_EVENTS[eventType]['handler'], str):
            self.process_listener_event(config.GATEWAY_EVENTS[eventType]['handler'], eventType, resourceObject)

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
                self.process_listener_event(handler, eventType, resourceObject)

    #-------------------------------------------------------------------------------------------
    def process_listener_event(self, handler, eventType: str, resourceObject: BaseResourceObject) -> None:
        if handler == "None":
            self.logQueue.put_nowait(LogEvent(component="HANDLER", action="LOG", level="DEBUG", message=f"[EventHandler] Event type {eventType} has no handler"))

        #-------------------------------------------
        # Check if the handler is HTTP
        #-------------------------------------------
        elif handler == "HTTP":
            for requestObject in self.botListeners.checkHttpListeners(resourceObject):
                newReq = HttpEvent(data=requestObject)
                self.httpQueue.put_nowait(newReq)

        #-------------------------------------------
        # Check if the handler is DB.
        # No handler should be DB if the database
        # has not been configured in the conf file.
        #-------------------------------------------
        elif handler == "DB":
            if not config.OPTS['database']:
                self.logQueue.put_nowait(LogEvent(component="HANDLER", action="LOG", level="ERROR", message=f"[EventHandler] Event type {eventType} has DB handler but no database configured"))
                return
            dbEvent = DatabaseEvent(action="DB")
            if "CREATE" in eventType or "UPDATE" in eventType:
                dbEvent.operation = "upsert"
                dbEvent.data['objData'] = resourceObject

            elif "DELETE" in eventType:
                dbEvent.operation = "delete"
                dbEvent.data['id'] = resourceObject.id

            if eventType.startswith("GUILD_"):
                if eventType.startswith("GUILD_MEMBER_"):
                    dbEvent.table = "guild_member"
                else:
                    dbEvent.table = "guild"
            elif eventType.startswith("USER_"):
                dbEvent.table = "user"
            elif eventType.startswith("MESSAGE_"):
                dbEvent.table = "message"
            elif eventType.startswith("CHANNEL_"):
                dbEvent.table = "channel"
            elif "ROLE_" in eventType:
                dbEvent.table = "role"

            self.dbRequestQueue.put_nowait(dbEvent)