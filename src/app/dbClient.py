import config
import time
import queue
from multiprocessing import Process, JoinableQueue
from src.models.procs.event import ProcessEvent, LogEvent, DatabaseEvent
from src.db.core import Database

class DBClient(Process):
    '''
        DBClient is a Process that handles database operations for the bot.
        It listens for DatabaseEvent objects on the dbQueue and processes them.

        Attributes:
            botQueue (JoinableQueue): Queue for communication with the main bot process.
            logQueue (JoinableQueue): Queue for logging events.
            dbQueue (JoinableQueue): Queue for database events.

        Methods:
            run() -> None: The main loop that processes database events.
    '''
    def __init__(self, name, botQueue, logQueue, dbRequestQueue, dbResponseQueue):
        super().__init__(name=name)

        self.killDbClient = False
        self.botQueue = botQueue
        self.logQueue = logQueue
        self.dbRequestQueue = dbRequestQueue
        self.dbResponseQueue = dbResponseQueue
        self.db = Database(logQueue)

    #-------------------------------------------------------------------------------------------
    def run(self):
        while True:
            try:
                evnt = self.dbRequestQueue.get_nowait()
                self.dbRequestQueue.task_done()

            except queue.Empty:
                time.sleep(0.001)
                continue

            if evnt.action == "STOP":
                self.killDbClient = True
                break

            elif evnt.action == "DB":
                result = self.processEvent(evnt)

                if evnt.response is not None:
                    self.dbResponseQueue.put_nowait(DatabaseEvent.create_response(evnt, result))

        self.db.engine.close()
        self.botQueue.put_nowait(ProcessEvent("DB", "STOPPED"))

    #-------------------------------------------------------------------------------------------
    def processEvent(self, evnt):
        '''
            Process a DatabaseEvent object.
        '''
        result = self.db.execute(evnt)
        return result