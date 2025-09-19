import time
import config
import queue
from typing import Dict

from multiprocessing import Process, JoinableQueue
from src.app.gatewayClient import GatewayClient
from src.app.loggerClient import LoggerClient
from src.app.httpClient import HttpClient
from src.app.dbClient import DBClient
from src.app.handlerClient import HandlerClient
from src.models.procs.event import ProcessEvent

config._prepare_config()

class BotClient():
    '''
        Accepts no arguments and initializes the bot client.
        This class manages the bot's processes, including the gateway, logger, and HTTP client.

        It provides methods to start and stop the bot client, manage processes, and handle events.
        Events are communicated through a `JoinableQueue`, allowing for inter-process communication.

        Attributes:
            botQueue (JoinableQueue): Queue for managing bot events and process communication.
            processes (Dict[str, dict]): Dictionary to hold process objects and their statuses.
            queues (Dict[str, JoinableQueue]): Dictionary to hold queues for different processes.

        Methods:
            start()                     -> None: Starts the bot client and manages the event loop.
            stop()                      -> None: Stops all processes and cleans up resources.
            uninitializedBotClient()    -> None: Cleans up resources and stops all processes.
            initializeBotClient()       -> None: Initializes the bot client and starts necessary processes.
            manageProcs()               -> None: Checks and manages the status of processes, restarting them if necessary.
            newProc(procName)           -> Process: Creates a new process based on the provided process name and returns the process object.

        Attribute Layout:
            In each of these attributes, ClientType refers to the type of client (e.g., 'GATEWAY', 'LOGGER', 'HTTP'),
            -----------
            botQueue: JoinableQueue, used for communication between the main bot process and all of the sub-processes for each client type.
            -----------
            queues: Dict,  { ClientType, JoinableQueue }
            -----------
            processes: Dict, { ClientType, {'proc': Process, 'status': str} }
                       Process statuses: 'running', 'stopped', 'failed'
    '''

    __slots__ = ('botQueue', 'processes', 'queues')

    def __init__(self):
        self.botQueue: JoinableQueue = JoinableQueue()
        self.processes: Dict[str, dict] = dict()
        self.queues: Dict[str, JoinableQueue] = dict()

    #-------------------------------------------------------------------------------------------
    def start(self) -> None:
        '''
            Start the bot client.
            This method initializes the bot client, starts the necessary processes, and manages the event loop.

            TODO: Exit gracefully on SIGINT or SIGTERM.
        '''
        self.initializeBotClient()

        while True:
            time.sleep(0.001)
            self.manageProcs()

            try:
                procEvent = self.botQueue.get_nowait()
                self.botQueue.task_done()

            except queue.Empty:
                continue

            if procEvent.action == "GATEWAY_ERROR":
                self.uninitializedBotClient()
                self.initializeBotClient()

        self.uninitializedBotClient()

    #-------------------------------------------------------------------------------------------
    def stop(self) -> None:
        for procName, procObj in self.processes.items():
            if procObj['status'] == 'running':
                procEvent = ProcessEvent(procName, "STOP")
                self.queues[procName].put_nowait(procEvent)

    #-------------------------------------------------------------------------------------------
    def uninitializedBotClient(self) -> None:
        '''
            Cleans up resources and stops all processes.
            This method ensures that all processes are terminated and resources are released.
        '''
        self.stop()

        for queueName, queueObj in self.queues.items():
            queueObj.join()
            queueObj.close()

        for procName, procObj in self.processes.items():
            if procObj['proc'] is not None:
                procObj['proc'].terminate()
                procObj['proc'].join()
                procObj['proc'] = None
                procObj['status'] = 'stopped'

    #-------------------------------------------------------------------------------------------
    def initializeBotClient(self) -> None:
        '''
            Initializes the bot client and starts necessary processes.
            This method sets up the queues and processes required for the bot client to function.
        '''
        #-----------------------------------------------------------------
        # Initialize the queues for each process type.
        # Each process will have its own queue for communication.
        # NOTE: These need to be initialized before even creating the new
        # processes because they are passed to the process constructors.
        #-----------------------------------------------------------------
        self.queues = {
            'LOGGER': JoinableQueue(),
            'GATEWAY': JoinableQueue(),
            'HTTP': JoinableQueue(),
            'HTTP_RESPONSE': JoinableQueue(),
            'HANDLER': JoinableQueue()
        }

        #-----------------------------------------------------------------
        # If the database configuration is not provided, remove the DB and
        # DB_RESPONSE queues from the queues dictionary.
        #-----------------------------------------------------------------
        if config.OPTS['database']:
            self.queues['DB'] = JoinableQueue()
            self.queues['DB_RESPONSE'] = JoinableQueue()

        else:
            self.queues['DB'] = None
            self.queues['DB_RESPONSE'] = None

        #-----------------------------------------------------------------
        # Initialize the processes dictionary with processes that have
        # not been started yet.
        #-----------------------------------------------------------------
        self.processes = {
            "GATEWAY": {'proc': self.newProc("GATEWAY"), 'status': 'stopped'},
            "LOGGER": {'proc': self.newProc("LOGGER"), 'status': 'stopped'},
            "HTTP": {'proc': self.newProc("HTTP"), 'status': 'stopped'},
            "HANDLER": {'proc': self.newProc("HANDLER"), 'status': 'stopped'}
        }

        if config.OPTS['database']:
            self.processes["DB"] = {'proc': self.newProc("DB"), 'status': 'stopped'}

        #-----------------------------------------------------------------
        # Start all processes that have been initialized.
        # This will start the processes that have been created in the
        # processes dictionary.
        #-----------------------------------------------------------------
        for procName, procObj in self.processes.items():
            if procObj['proc'] is not None:
                procObj['proc'].start()
                procObj['status'] = 'running'
                print(f"Started {procName} process - pid {procObj['proc'].pid}")

    #-------------------------------------------------------------------------------------------
    def manageProcs(self) -> None:
        '''
            Actively checks for processes that have been stopped and removes them from the list,
            then recreates and starts them as needed.
            This method ensures that all processes are running and handles any necessary restarts.
        '''
        for procName, procObj in self.processes.items():
            if procObj['status'] == 'finished':
                if procObj['proc'] is not None:
                    procObj['proc'].join()
                    procObj['proc'] = None
                    procObj['status'] = 'stopped'
            #---------------------------------------------------------------
            # Check if the process is not alive and restart it.
            # This can happen if the process has crashed or been terminated.
            #---------------------------------------------------------------
            if not procObj['proc'].is_alive():
                procObj['proc'].terminate()
                procObj['proc'].join()
                procObj['proc'] = None
                newProc = self.newProc(procName)
                self.processes[procName] = {'proc': newProc, 'status': 'running'}
                newProc.start()

    #-------------------------------------------------------------------------------------------
    def newProc(self, procName) -> Process:
        '''
            Creates a new process based on the provided process name and returns the process object.
            This method is responsible for initializing the appropriate client based on the process name.
        '''
        if procName == 'GATEWAY':
            newGateClient = GatewayClient("GATEWAY",
                                          self.botQueue,
                                          self.queues['HANDLER'],
                                          self.queues['GATEWAY'],
                                          self.queues['LOGGER'],
                                          self.queues['DB'],
                                          self.queues['DB_RESPONSE'],
                                          self.queues['HTTP'],
                                          self.queues['HTTP_RESPONSE'])
            return newGateClient

        if procName == 'LOGGER':
            newLoggerClient = LoggerClient("LOGGER",
                                           self.botQueue,
                                           self.queues['LOGGER'])
            return newLoggerClient

        if procName == 'HTTP':
            newHttpClient = HttpClient("HTTP",
                                        self.botQueue,
                                        self.queues['LOGGER'],
                                        self.queues['HTTP'],
                                        self.queues['HTTP_RESPONSE'])
            return newHttpClient

        if procName == 'DB':
            newDbClient = DBClient("DB",
                                    self.botQueue,
                                    self.queues['LOGGER'],
                                    self.queues['DB'],
                                    self.queues['DB_RESPONSE'])
            return newDbClient

        if procName == "HANDLER":
            newHandlerClient = HandlerClient("HANDLER",
                                              self.queues['HANDLER'],
                                              self.queues['LOGGER'],
                                              self.queues['HTTP'],
                                              self.queues['HTTP_RESPONSE'],
                                              self.queues['DB'],
                                              self.queues['DB_RESPONSE'])
            return newHandlerClient