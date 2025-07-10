import time
import config
import queue
from typing import Dict

from multiprocessing import Process, JoinableQueue
from src.app.gatewayClient import GatewayClient
from src.app.loggerClient import LoggerClient
from src.app.httpClient import HttpClient
from src.app.dbClient import DBClient
from src.models.procs.event import ProcessEvent

config._prepare_config()

class BotClient():

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
        self.queues = {
            'LOGGER': JoinableQueue(),
            'DB': JoinableQueue(),
            'GATEWAY': JoinableQueue(),
            'HTTP': JoinableQueue()
        }

        self.processes = {
            "GATEWAY": {'proc': self.newProc("GATEWAY"), 'status': 'stopped'},
            "LOGGER": {'proc': self.newProc("LOGGER"), 'status': 'stopped'},
            "HTTP": {'proc': self.newProc("HTTP"), 'status': 'stopped'},
        }

        for procName, procObj in self.processes.items():
            if procObj['proc'] is not None:
                procObj['proc'].start()
                procObj['status'] = 'running'
                print(f"Started {procName} process - pid {procObj['proc'].pid}")

    #-------------------------------------------------------------------------------------------
    def manageProcs(self) -> None:
        for procName, procObj in self.processes.items():
            if procObj['status'] == 'finished':
                if procObj['proc'] is not None:
                    procObj['proc'].join()
                    procObj['proc'] = None
                    procObj['status'] = 'stopped'
                    
            if not procObj['proc'].is_alive():
                procObj['proc'].terminate()
                procObj['proc'].join()
                procObj['proc'] = None
                newProc = self.newProc(procName)
                self.processes[procName] = {'proc': newProc, 'status': 'running'}
                newProc.start()

    #-------------------------------------------------------------------------------------------
    def newProc(self, procName) -> Process:
        if procName == 'GATEWAY':
            newGateClient = GatewayClient(self.botQueue, self.queues['GATEWAY'], self.queues['LOGGER'], self.queues['DB'], self.queues['HTTP'])
            return newGateClient

        if procName == 'LOGGER':
            newLoggerClient = LoggerClient(self.botQueue, self.queues['LOGGER'])
            return newLoggerClient
                
        if procName == 'HTTP':
            newHttpClient = HttpClient(self.botQueue, self.queues['LOGGER'], self.queues['HTTP'])
            return newHttpClient