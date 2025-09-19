import asyncio
import websockets
import time
import config
import queue

from multiprocessing import Process, JoinableQueue

from src.ext.generator import EventGenerator
from src.models.procs.event import ProcessEvent, LogEvent, HandlerEvent


__all__ = ['GatewayClient', 'GatewayListener', 'ReconnectWebSocket']

#-----------------------------------------------------------------------------------------------------------
class ReconnectWebSocket(Exception):
    """
        Signals to safely reconnect the websocket.
    """
    __slots__ = ('resume', 'shard_id', 'op')

    def __init__(self, shard_id = None, resume = True) -> None:
        self.shard_id   = shard_id
        self.resume     = resume
        self.op         = 'RESUME' if resume else 'IDENTIFY'

#-----------------------------------------------------------------------------------------------------------
class GatewayClient(Process):
    '''
        Manages the process related to connecting to the Discord Gateway API and receiving events from it.
        This class is a Process that runs the GatewayListener, which connects to the Discord Gateway API via websockets and asyncio.
        
        The reason it is split into a separate process is so that the main websocket event loop can be managed without blocking the main bot process.
        It also allows us to write other client processes for other uses such as logging, database access, etc.

        Recieves events from the botQueue for communication between the main process and itself.
    '''
    __slots__ = ('gatewayQueue', 'botQueue', 'listenerQueue', 'GatewayListener')

    def __init__(self, name, botQueue, handlerQueue, gatewayQueue, logQueue, dbRequestQueue, dbResponseQueue, httpQueue, httpResponseQueue):
        super().__init__(name=name)
        self.gatewayQueue = gatewayQueue
        self.botQueue = botQueue
        self.listenerQueue = JoinableQueue()
        self.GatewayListener = GatewayListener(logQueue, handlerQueue, dbRequestQueue, dbResponseQueue, httpQueue, httpResponseQueue, self.listenerQueue)

    #-------------------------------------------------------------------------------------------
    def run(self) -> None:
        '''
            Starts the GatewayListener process which connects to the Discord Gateway API via websockets and asyncio.
            The reason for it being split into a separate process is to allow for the main bot process to continue running while the GatewayListener handles events asynchronously.
            Unfuntately, for all its bonuses, asyncio will still block the main process if it is run in the same process as the bot.

            The GatewayListener will handle all events from the Gateway API and pass them to the EventHandler for processing.
            It will also handle the heartbeat and reconnection logic for the websocket connection.
        '''
        gatewayProc = Process(target = self.GatewayListener.asyncRunner)
        gatewayProc.start()

        while True:
            try:
                evnt = self.gatewayQueue.get_nowait()
                self.gatewayQueue.task_done()

            except queue.Empty:
                procCheck = self.checkGatewayProcess(gatewayProc)
                if procCheck is not None:
                    gatewayProc = procCheck
                time.sleep(0.01)
                continue

            if evnt.action == "STOP":
                self.listenerQueue.put_nowait(None)
                self.listenerQueue.join()
                gatewayProc.terminate()
                gatewayProc.join()
                gatewayProc = None
                break

        procEvent = ProcessEvent("GATEWAY", "STOPPED")
        self.botQueue.put_nowait(procEvent)

    #-------------------------------------------------------------------------------------------
    def checkGatewayProcess(self, proc) -> Process:
        '''
            Determines if the GatewayListener process is still alive.
            If it is not alive, it will terminate the process and start a new one.
        '''
        if proc.is_alive():
            return

        elif not proc.is_alive():
            proc.terminate()
            proc.join()
            proc = Process(target = self.GatewayListener.asyncRunner)
            proc.start()
            return proc

#-----------------------------------------------------------------------------------------------------------
class GatewayListener():
    '''
        Starts the two processes for interacting with the Discord Gateway API.
        Both processes are placed on the event loop for asyncio to handle.

        The first handles the heartbeat and reconnection logic for the websocket connection.
        The second handles the events from the Gateway API and passes them to the EventHandler for processing.
    '''
    __slots__ = ('logQueue', 
                    'httpQueue', 
                    'handlerQueue', 
                    'listenerQueue', 
                    'interval', 
                    'sequence', 
                    'session_id', 
                    'shard', 
                    'resume_gateway_url', 
                    'websocket')

    def __init__(self, logQueue, handlerQueue, dbRequestQueue, dbResponseQueue, httpQueue, httpResponseQueue, listenerQueue):
        self.logQueue: JoinableQueue = logQueue
        self.httpQueue: JoinableQueue = httpQueue
        self.handlerQueue: JoinableQueue = handlerQueue
        self.listenerQueue: JoinableQueue = listenerQueue

        self.interval = None
        self.sequence = None
        self.session_id = None
        self.shard = list()
        self.resume_gateway_url = ""
        self.websocket = None

    #-------------------------------------------------------------------------------------------
    def asyncRunner(self) -> None:
        '''
            Starts the AsyncIO Loop which connects directly to the
            Gateway API Websocket
        '''
        asyncio.run(self.socketClient())

    #-------------------------------------------------------------------------------------------
    # Main loop for the bot
    #-------------------------------------------------------------------------------------------
    async def socketClient(self) -> None:
        '''
            Main loop for the bot
        '''
        while True:

            #----------------------------------------
            #   Check for a stop signal
            #----------------------------------------
            try:
                finish = self.listenerQueue.get_nowait()
                self.listenerQueue.task_done()
                if finish is None:
                    return
            except queue.Empty:
                pass

            #----------------------------------------
            #   If the websocket is not connected
            #   then connect to the gateway
            #----------------------------------------
            if self.websocket is None:
                await self.connect()

            #----------------------------------------
            #   Run both the heartbeat response and
            #   the receive api in parallel
            #----------------------------------------
            try:
                await asyncio.gather(self.heartbeat(), self.receive())
            
            #----------------------------------------
            #   If the connection is lost, reconnect
            #----------------------------------------
            except ReconnectWebSocket as e:
                self.logQueue.put_nowait(LogEvent(component="GATEWAY", action="LOG", level="INFO", message="Reconnecting"))
                await self.websocket.close()
                
                if e.resume:
                    await self.resume()
                
                else:
                    self.websocket = None
            
            #----------------------------------------
            #   If the connection is closed, 
            #   reconnect or stop the loop and
            #   return which should recreate the
            #   process.
            #----------------------------------------
            except websockets.exceptions.ConnectionClosed as e:
                if e.code in config.RESPONSE_CODES.gateway_close_codes:
                    closeCode = config.RESPONSE_CODES.gateway_close_codes[e.code]

                else:
                    self.logQueue.put_nowait(LogEvent(component="GATEWAY", action="LOG", level="ERROR", message=f"[GatewayClient] Websocket Connection Closed, code: {e.code}, which isnt in the known error codes."))
                    return

                self.logQueue.put_nowait(LogEvent(component="GATEWAY", action="LOG", level="INFO", message=f"[GatewayClient] Connection Close Frame was sent: {closeCode._to_dict()}"))
                if closeCode.reconnect:

                    #-----------------------------------------
                    #   Check the code sent to the client
                    #   and determine if we should resume or
                    #   reconnect.
                    #------------------------------------------
                    if closeCode.code in [4001,4002,4008,1006]:
                        await self.resume()

                    if closeCode.code in [4000, 4009]:
                        self.logQueue.put_nowait(LogEvent(component="GATEWAY", action="LOG", level="INFO", message="[GatewayClient] Reconnecting in 5 seconds"))
                        self.websocket = None
                        await asyncio.sleep(5)

                    if closeCode.code in [4003, 4004, 4010, 4011, 4012, 4013, 4014]:
                        self.logQueue.put_nowait(LogEvent(component="GATEWAY", action="LOG", level="INFO", message="[GatewayClient] Problem bad, shouldnt reconnect"))
                        return
                else:
                    return

    #--------------------------------------------------------------------------------
    # Receive loop
    #--------------------------------------------------------------------------------
    async def receive(self) -> None:
        '''
            Recieves Gatewayy Events as dictionaries.

            {
                "op": 0,
                "d": {},
                "s": 42,
                "t": "GATEWAY_EVENT_NAME"
            }

            op -> The opcode for the event
            d -> The data for the event
            s -> The sequence number for the event
            t -> The event name
        '''
        async for message in self.websocket:
            #----------------------------------------
            #   Get the incoming message from the 
            #   async generator and create a 
            # GatewayEvent object from it.
            #----------------------------------------
            evnt = EventGenerator.incoming_event(message)

            if evnt is None:
                self.logQueue.put_nowait(LogEvent(component="GATEWAY", action="LOG", level="ERROR", message="[GatewayClient] Received None from incoming_event"))
                continue

            # for debugging
            #self.logQueue.put_nowait(LogEvent(action="LOG", level="INFO", message=f"[GatewayClient] {evnt._to_dict()}"))

            #----------------------------------------
            #   Get the OpCode object from the
            #   config module.
            #----------------------------------------
            try:
                opCode = config.RESPONSE_CODES.gateway_op_codes[evnt.op]

            except KeyError:
                self.logQueue.put_nowait(LogEvent(component="GATEWAY", action="LOG", level="ERROR", message=f"[GatewayClient] Unknown OpCode -- {evnt._to_dict()}"))
                continue

            #----------------------------------------
            #   Heartbeat Event
            #----------------------------------------
            if opCode.name == "Heartbeat":
                heart_event = EventGenerator.heartbeat_event(self.sequence)
                await self.websocket.send(heart_event._to_payload())

            #----------------------------------------
            #   InvalidSession Event
            #----------------------------------------
            if opCode.name == "Invalid Session":
                raise ReconnectWebSocket(resume = False)

            #----------------------------------------
            #   Reconnect Event
            #----------------------------------------
            if opCode.name == "Reconnect":
                raise ReconnectWebSocket()

            #----------------------------------------------------------------------
            #   Dispatch Event
            #   Only Dispatch events are not related
            #   to the websocket connection.
            #----------------------------------------------------------------------
            if opCode.name == "Dispatch":
                self.sequence = int(evnt.s)

                if evnt.t == "READY":
                    self.session_id = evnt.d["session_id"]
                    self.resume_gateway_url = f'{evnt.d["resume_gateway_url"]}/?v=6&encoding=json'

                    if "shard" in evnt.d:
                        self.shard = evnt.d["shard"]

                    self.logQueue.put_nowait(LogEvent(component="GATEWAY", action="LOG", level="INFO", message=f"[GatewayClient] Got session ID: {self.session_id}"))

                elif evnt.t == "RESUMED":
                    self.logQueue.put_nowait(LogEvent(component="GATEWAY", action="LOG", level="INFO", message="[GatewayClient] Successfully resumed"))

                #----------------------------------------------------------------------
                #   All other events before this point
                #   are for maintaining the websocket
                #   connection.
                #----------------------------------------------------------------------
                else:
                    #----------------------------------------
                    #   Skip events from the bot
                    #----------------------------------------
                    if 'author' in evnt.d and evnt.d['author']['id'] == config.OPTS['appId']:
                        continue

                    discordResource = EventGenerator.createResource(evnt)

                    #----------------------------------------
                    #   If the resource is None, then we
                    #   could not create a resource for the
                    #   event type. So it is not supported.
                    #   See the event_map in the generater.py
                    #   file for the supported event types.
                    #-----------------------------------------
                    if discordResource is None:
                        self.logQueue.put_nowait(LogEvent(component="GATEWAY", action="LOG", level="ERROR", message=f"[GatewayClient] Could not create resource for event: {evnt.t}"))
                        continue

                    self.logQueue.put_nowait(LogEvent(component="GATEWAY", action="LOG", level="DEBUG", message=f"[GatewayClient] Dispatching event: {evnt.t}\n{discordResource._to_dict()}"))
                    self.handlerQueue.put_nowait(HandlerEvent(eventType=evnt.t, resourceObject=discordResource))

    #-------------------------------------------------------------------------------------------
    # Heartbeat loop
    #-------------------------------------------------------------------------------------------
    async def heartbeat(self) -> None:
        while self.interval is not None:
            evnt = EventGenerator.heartbeat_event(self.sequence)
            await self.websocket.send(evnt._to_payload())
            await asyncio.sleep(self.interval)
    
    #-------------------------------------------------------------------------------------------
    # Resume the connection
    #-------------------------------------------------------------------------------------------
    async def resume(self) -> None:
        self.logQueue.put_nowait(LogEvent(component="GATEWAY", action="LOG", level="DEBUG", message="[GatewayClient] Attempting to resume connection"))
        self.websocket = await websockets.connect(self.resume_gateway_url)
        evnt = EventGenerator.resume_event(self.sequence, self.session_id)
        await self.websocket.send(evnt._to_payload())

    #-------------------------------------------------------------------------------------------
    # Connect
    #-------------------------------------------------------------------------------------------
    async def connect(self) -> None:
        self.websocket = await websockets.connect('wss://gateway.discord.gg/?v=6&encoding=json')
        #----------------------------------------
        # inital handshake
        #----------------------------------------
        await self.identify()

    #-------------------------------------------------------------------------------------------
    # Handshake and authentication
    #-------------------------------------------------------------------------------------------
    async def identify(self) -> None:
        self.logQueue.put_nowait(LogEvent(component="GATEWAY", action="LOG", level="INFO", message="[GatewayClient] Attempting Handshake and authentication"))
        await self.websocket.send(EventGenerator.auth_event()._to_payload())

        ret = await self.websocket.recv()
        evnt = EventGenerator.incoming_event(ret)

        if evnt.op != 10:
            self.logQueue.put_nowait(LogEvent(component="GATEWAY", action="LOG", level="INFO", message="[GatewayClient] Unexpected reply"))
            self.logQueue.put_nowait(LogEvent(component="GATEWAY", action="LOG", level="DEBUG", message=ret))

        if evnt.op == 10:
            self.logQueue.put_nowait(LogEvent(component="GATEWAY", action="LOG", level="INFO", message="[GatewayClient] Authenticated"))

        self.interval = evnt.d["heartbeat_interval"] / 1000
        self.logQueue.put_nowait(LogEvent(component="GATEWAY", action="LOG", level="INFO", message=f"[GatewayClient] interval: {self.interval}"))
