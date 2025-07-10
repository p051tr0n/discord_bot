import asyncio
import websockets
import time
import config
import queue

from multiprocessing import Process, JoinableQueue

from src.ext.generator import EventGenerator
from src.ext.handler import EventHandler
from src.models.procs.event import ProcessEvent, LogEvent



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
# NOTE: This class should be reworked.  There is probably no need to have it split into two processes.

class GatewayClient(Process):
    '''
        Manages the process related to connecting to the Discord Gateway API and receiving events from it.

        Recieves events from the botQueue for communication between the main process and itself.
    '''
    __slots__ = ('gatewayQueue', 'botQueue', 'listenerQueue', 'GatewayListener')

    def __init__(self, botQueue, gatewayQueue, logQueue, dbQueue, httpQueue):
        super().__init__()
        self.gatewayQueue = gatewayQueue
        self.botQueue = botQueue
        self.listenerQueue = JoinableQueue()
        self.GatewayListener = GatewayListener(logQueue, dbQueue, httpQueue, self.listenerQueue)

    #-------------------------------------------------------------------------------------------
    def run(self) -> None:
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
    '''
    __slots__ = ('logQueue', 
                    'dbQueue', 
                    'httpQueue', 
                    'listenerQueue', 
                    'interval', 
                    'sequence', 
                    'session_id', 
                    'shard', 
                    'resume_gateway_url', 
                    'websocket', 
                    'evnt_handler')

    def __init__(self, logQueue, dbQueue, httpQueue, listenerQueue):
        self.logQueue: JoinableQueue = logQueue
        self.dbQueue: JoinableQueue = dbQueue
        self.httpQueue: JoinableQueue = httpQueue
        self.listenerQueue: JoinableQueue = listenerQueue

        self.interval = None
        self.sequence = None
        self.session_id = None
        self.shard = list()
        self.resume_gateway_url = ""
        self.websocket = None
        self.evnt_handler = EventHandler(logQueue, dbQueue, httpQueue)

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
                self.logQueue.put_nowait(LogEvent(action="LOG", level="INFO", message="Reconnecting"))
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
                    self.logQueue.put_nowait(LogEvent(action="LOG", level="ERROR", message=f"Websocket Connection Closed, code: {e.code}, which isnt in the known error codes."))
                    self.logQueue.put_nowait(LogEvent(action="LOG", level="ERROR", message="Killing Gateway Client due to unknown ConnectionClosed code"))
                    return

                self.logQueue.put_nowait(LogEvent(action="LOG", level="INFO", message=f"Connection Close Frame was sent: {closeCode._to_dict()}"))
                if closeCode.reconnect:

                    if closeCode.code in [4001,4002,4008,1006]:
                        await self.resume()

                    if closeCode.code in [4000, 4009]:
                        self.websocket = None
                        await asyncio.sleep(5)

                    if closeCode.code in [4003, 4004, 4010, 4011, 4012, 4013, 4014]:
                        self.logQueue.put_nowait(LogEvent(action="LOG", level="INFO", message="Problem bad, shouldnt reconnect"))
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
                self.logQueue.put_nowait(LogEvent(action="LOG", level="ERROR", message="Received None from incoming_event"))
                continue

            # for debugging
            self.logQueue.put_nowait(LogEvent(action="LOG", level="INFO", message=evnt._to_dict()))

            #----------------------------------------
            #   Get the OpCode object from the
            #   config module.
            #----------------------------------------
            try:
                opCode = config.RESPONSE_CODES.gateway_op_codes[evnt.op]

            except KeyError:
                self.logQueue.put_nowait(LogEvent(action="LOG", level="ERROR", message="Unknown OpCode"))
                self.logQueue.put_nowait(LogEvent(action="LOG", level="ERROR", message=evnt._to_dict()))
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

            #----------------------------------------
            #   Dispatch Event
            #----------------------------------------
            if opCode.name == "Dispatch":
                self.sequence = int(evnt.s)

                if evnt.t == "READY":
                    self.session_id = evnt.d["session_id"]
                    self.resume_gateway_url = f'{evnt.d["resume_gateway_url"]}/?v=6&encoding=json'
                    
                    if "shard" in evnt.d:
                        self.shard = evnt.d["shard"]

                    self.logQueue.put_nowait(LogEvent(action="LOG", level="INFO", message=f"Got session ID: {self.session_id}"))

                elif evnt.t == "RESUMED":
                    self.logQueue.put_nowait(LogEvent(action="LOG", level="INFO", message="Successfully resumed"))

                #----------------------------------------
                #   All other events before this point
                #   are for maintaining the websocket
                #   connection.
                #----------------------------------------
                else:
                    #----------------------------------------
                    #   If the event is from the bot, ignore
                    #----------------------------------------
                    if 'author' in evnt.d and evnt.d['author']['id'] == config.OPTS['appId']:
                        continue

                    self.evnt_handler.handle_event(evnt.t, EventGenerator.createResource(evnt))
    

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
        self.logQueue.put_nowait(LogEvent(action="LOG", level="DEBUG", message="Attempting to resume connection"))
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
        self.logQueue.put_nowait(LogEvent(action="LOG", level="INFO", message="Attempting Handshake and authentication"))
        await self.websocket.send(EventGenerator.auth_event()._to_payload())

        ret = await self.websocket.recv()
        evnt = EventGenerator.incoming_event(ret)

        if evnt.op != 10:
            self.logQueue.put_nowait(LogEvent(action="LOG", level="INFO", message="Unexpected reply"))
            self.logQueue.put_nowait(LogEvent(action="LOG", level="DEBUG", message=ret))
            self.botQueue.put_nowait(ProcessEvent(action="GATEWAY_WAY"))

        if evnt.op == 10:
            self.logQueue.put_nowait(LogEvent(action="LOG", level="INFO", message="Authenticated"))

        self.interval = evnt.d["heartbeat_interval"] / 1000
        self.logQueue.put_nowait(LogEvent(action="LOG", level="INFO", message=f"interval: {self.interval}"))
