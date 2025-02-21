import config
import queue
from multiprocessing import Process, JoinableQueue
from models.procs.event import ProcessEvent, LogEvent

#config._prepare_config()

class DBClient(Process):
    
    def __init__(self, botQueue, logQueue, dbQueue):
        super().__init__()

        self.killDbClient = False
        self.botQueue = botQueue
        self.logQueue = logQueue
        self.dbQueue = dbQueue

    #-------------------------------------------------------------------------------------------
    def run(self):
        while True:
            evnt = self.dbQueue.get()
            self.dbQueue.task_done()

            if evnt.action == "STOP":
                self.killDbClient = True
                break

            elif evnt.action == "DB":
                pass
                # Add in a handler here to handle HTTP requests
        
        procEvent = ProcessEvent("DB", "STOPPED")
        self.botQueue.put_nowait(procEvent)